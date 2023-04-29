#ShopWise Pantry.py
# ----- Entire code below  ------- #  

# ----- Import libraries  ------- #  
import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage
import gcsfs
import pandas as pd
from st_aggrid import AgGrid, JsCode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import gspread 
from gspread_pandas import Spread,Client
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame
import st_aggrid as st_ag

 
# ----- Page setup ----- #
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='wide')
st.title('Pantry')


# ----- Disable certificate verification (Not necessary always) ----- #
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# ----- Create a Google Authentication connection objectt ----- #
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)


# ----- Connect to the Google Shee ----- #
spreadsheetname = "ShopWise Food List"
spread = Spread(spreadsheetname,client = client)
sh = client.open(spreadsheetname)

sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
sheet_name = "Pantry"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
p_df = pd.read_csv(url, dtype=str).fillna("")

sheet_name2 = "Food_List_Master"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name2}"
fd_list_df = pd.read_csv(url, dtype=str).fillna("")


# ----- Creating functions ----- #
## Update to Sheet
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

## Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Item','Weight']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.success('Updated')
    
# ----- User add items to pantry ----- #
df = load_the_spreadsheet(sheet_name)

with st.form("form"):
    st.header('Add items below')
    item = st.selectbox('Food Item (type to search/use dropdown)',list(fd_list_df['Name'])) 
    weight = st.number_input("Weight(g)")
    add_submitted = st.form_submit_button("Add Item")
    
    if add_submitted:
        if len(df) == 0:
         user_input = {"Item": [item], "Weight": [weight]} # User input dataframe
         user_input_df = pd.DataFrame(user_input)
         update_the_spreadsheet('Pantry',user_input_df) # update google sheet
         
        else:
         user_input = [item, weight] # User input dataframe
         df.loc[len(df.index)] = user_input # insert usert input
         update_the_spreadsheet('Pantry',df) # update google sheet
         

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
                </style>
                <button id='click-button'
                    class="btn-danger"
                    > X </button>
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

    

 
# ----- 


annotated = st.experimental_data_editor(df)
add_submitted = st.button("Add Item")
if add_submitted:
         update_the_spreadsheet('Pantry',annotated) # update google sheet
else:
     st.write('Incorrect')
        
df = load_the_spreadsheet(sheet_name) #refresh google sheet
        
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True,groupable=True)






    
"""
# ----- Creating an interactive table ----- #

gd = GridOptionsBuilder.from_dataframe(df_selection)
gd.configure_pagination(enabled = True)
gd.configure_default_column(editable =True, groupable = True)


sel_mode = st.radio('Selection Type', options = ['Single', 'Multiple'])
gd.configure_selection(selection_mode = sel_mode, use_checkbox = True)
gridoptions = gd.build()
grid_table = AgGrid(df_selection, gridOptions = gridoptions,
                   update_mode = GridUpdateMode.SELECTION_CHANGED,
                   height = 500,
                   allow_unsafe_jscode = True)

sel_row = grid_table["selected_rows"]
st.write(sel_row)

# ----- Add items to the table ----- #

edited_df = st.experimental_data_editor(df, num_rows="dynamic")


# Functions 
@st.cache()
# Get our worksheet names
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Product_ID','Quantity','Purchase_Date']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')


with st.form("form"):
    item = st.selectbox('Food_List_Master',list(food_Item_df['Product_ID']))
    Quantity = st.number_input("Weight(g)")
    add_submitted = st.form_submit_button("Add Item")

    if add_submitted :  
                  now = datetime.now()
                  opt = {'Product_ID': [item],
                         'Quantity': [Quantity],
                         'Purchase_Date' : [now]} 
                  opt_df = DataFrame(opt)
                  df = load_the_spreadsheet('Pantry_Loc_Line')
                  new_df = df.append(opt_df,ignore_index=True)
                  update_the_spreadsheet('Pantry_Loc_Line',new_df)
   
"""
