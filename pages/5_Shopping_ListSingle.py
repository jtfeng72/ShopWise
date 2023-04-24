#ShopWise.py
#---Import libraries---#
from google.oauth2 import service_account
from gspread_pandas import Spread,Client
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.title('Shopping List')

# Disable certificate verification (Not necessary always)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# --- Create a Google Authentication connection objectt --- #
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "ShopWise Food List"
spread = Spread(spreadsheetname,client = client)

#st.write(spread.url)

# --- Call the spreadshet --- #
sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
sheet_name = "Shopping_List2"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
url2= "https://raw.githubusercontent.com/jtfeng72/ShopWise/master/Data/ShopWise%20Food%20List.csv"
sl_df = pd.read_csv(url, dtype=str).fillna("")

food_Item_dd = pd.read_csv(url2)

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Purchase_dt','Item','Weight']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')

#Display the latest update
df = load_the_spreadsheet(sheet_name)

st.write(df)

with st.form("form"):
    st.header('Add items below')
    purchase_dt = st.date_input("Date of Purchase")
    item = st.selectbox('Food_List_Master',list(food_Item_dd['Name'])) 
    weight = st.number_input("Weight(g)")
    add_submitted = st.form_submit_button("Add Item")
    
    if add_submitted:
        if len(df) == 0:
         user_input = { "Purchase_dt": [purchase_dt], "Item": [item], "Weight": [weight]} # User input dataframe
         user_input_df = pd.DataFrame(user_input)
         update_the_spreadsheet('Shopping_List2',user_input_df) # update google sheet
         
        else:
         user_input = [purchase_dt, item, weight] # User input dataframe
         df.loc[len(df.index)] = user_input # insert usert input
         update_the_spreadsheet('Shopping_List2',df) # update google sheet

df = load_the_spreadsheet(sheet_name) #refresh google sheet
        
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True,groupable=True)

#  --- JavaScript function to add a new row to the AgGrid table ---         
js_del_row = JsCode ('''
function(e) {
 let api = e.api;
 let sel = api.getSelectedRows(); 
 api.applyTransaction({remove: sel}) 
};
'''
)

#  --- Cell renderer for the '🔧' column to render a button --- 
cellRenderer_addButton = JsCode('''
    class BtnCellRenderer {
        init(params) {
            this.params = params;
            this.eGui = document.createElement('div');
            this.eGui.innerHTML = `
            <span>
                <style>
                .btn_add {
                    background-color: red;
                    border: 2px solid black;
                    color: white;
                    text-align: center;
                    display: inline-block;
                    font-size: 12px;
                    font-weight: bold;
                    height: 2em;
                    width: 10em;
                    border-radius: 12px;
                    padding: 0px;
                }
                </style>
                <button id='click-button' 
                    class="btn_add" 
                    > Remove</button>
            </span>
        `;
        }
        getGui() {
            return this.eGui;
        }
    };
    ''')         
    
gd.configure_selection(selection_mode= 'single')
#gd.configure_grid_options(onRowSelected = js_del_row,pre_selected_rows=[])
gd.configure_column( field = '🔧', 
                     onCellClicked = js_del_row,      #adding delete function into the button
                     pre_selected_rows=[],
                     cellRenderer = cellRenderer_addButton, #adding the button desgin
                     lockPosition='left')
gridOptions = gd.build()


with st.form('Shopping List') as f:
         st.header('Shopping List 🔖')
         grid_table = AgGrid(df, 
                   gridOptions = gridOptions, 
                   fit_columns_on_grid_load = True,
                   theme = "streamlit",
                   allow_unsafe_jscode=True,
                   )
         st.info("Total Rows :" + str(len(grid_table['data'])))
         
         submitted = st.form_submit_button("Confirm item(s) 🔒")
         
         df_final = grid_table["data"].columns[1:]
         df_final
         
         if submitted:
                  update_the_spreadsheet('Shopping_List2',df_final) # update google sheet
