#ShopWise.py
#---Import libraries---#
from google.oauth2 import service_account
from gspread_pandas import Spread,Client
import pandas as pd
import streamlit as st
import gspread 
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

#---gc update---#
gc = gspread.authorize(credentials)
s = gc.open("ShopWise Food List") # open your spreadsheet
w = s.worksheet("Shopping_List2") # get data from "Shopping_List2" tab

# --- Call the spreadshet --- #
sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
#connection to the Shopping list table
sl_line_sheet = "Shopping_List2"#"Shopping_List_Line"
sl_line_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sl_line_sheet}"
sl_line_df = pd.read_csv(sl_line_url, dtype=str).fillna("")

#get all avaliable food items from master list for drop down features
fd_list_sheet = "Food_List_Master"
fd_list_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={fd_list_sheet}"
fd_list_df = pd.read_csv(fd_list_url, dtype=str).fillna("")

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Item','Weight']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.success('Updated')

#Display the latest update
df = load_the_spreadsheet(sl_line_sheet)

with st.form("form"):
    st.header('Add items below')
    #purchase_dt = st.date_input("Date of Purchase")
    item = st.selectbox('Food_Item',list(fd_list_df['Name'])) 
    weight = st.number_input("Weight(g)")
    add_submitted = st.form_submit_button("Add Item")
    
    if add_submitted:
        if len(df) == 0:
         user_input = {"Item": [item], "Weight": [weight]} # User input dataframe
         user_input_df = pd.DataFrame(user_input)
         update_the_spreadsheet('Shopping_List2',user_input_df) # update google sheet
         
        else:
         user_input = [item, weight] # User input dataframe
         df.loc[len(df.index)] = user_input # insert usert input
         update_the_spreadsheet('Shopping_List2',df) # update google sheet
         

df = load_the_spreadsheet(sl_line_sheet) #refresh google sheet
        
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
gd.configure_column( field = 'Click to Remove', 
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
         
         if submitted:
                  df_final = grid_table["data"]
                  st.write (df_final)
                  spread.clear_sheet(sheet = spreadsheetname)
                  update_the_spreadsheet('Shopping_List2',df_final) # update google sheet
         
         #if submitted:
                  #df_final = grid_table["data"]

                  #for ind in df_final.index:
                           #values_list = w.col_values(1)
                           #length_row = len(values_list)
                           #w.update_cell(length_row+1, 1, str(df_final ['Item'][ind]))
                           #w.update_cell(length_row+1, 2, str(df_final ['Weight'][ind]))
