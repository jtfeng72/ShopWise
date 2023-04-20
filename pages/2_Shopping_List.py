#ShopWise.py
#---Import libraries---#
from collections import namedtuple
from google.oauth2 import service_account
from gspread_pandas import Spread,Client
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.title('Shopping List')
st.header('Add items below')

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

df = load_the_spreadsheet(sheet_name)

with st.form("form"):
    purchase_dt = st.date_input("Date of Purchase")
    item = st.selectbox('Food_List_Master',list(food_Item_dd['Name'])) 
    weight = st.number_input("Weight(g)")
    submitted = st.form_submit_button("Add Item")
    
    if submitted:
        opt = { "Purchase_dt": [purchase_dt], "Item": [item], "Weight": [weight]}
        opt_df = pd.DataFrame(opt)
        df2 = load_the_spreadsheet(sheet_name)
        new_df = df2.append(opt_df,ignore_index=True)
        update_the_spreadsheet('Shopping_List2',new_df)
        
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
gd.configure_grid_options(onRowSelected = js_del_row,pre_selected_rows=[])
gridOptions = gd.build()


st.header('Shopping List 🔖')
grid_table = AgGrid(df, 
          gridOptions = gridOptions, 
          enable_enterprise_modules = True,
          fit_columns_on_grid_load = True,
          height=500,
          width='100%',
          # theme = "streamlit",
          update_mode = GridUpdateMode.SELECTION_CHANGED,
          reload_data = True,
          allow_unsafe_jscode=True,
          )
st.info("Total Rows :" + str(len(grid_table['data'])))


