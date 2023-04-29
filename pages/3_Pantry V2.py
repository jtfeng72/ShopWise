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
## Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    load_df = pd.DataFrame(worksheet.get_all_records())
    return load_df

## Update add to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Item','Weight']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.success('Updated')

## Update annotated Sheet
def update_annotated_spreadsheet(spreadsheetname,dataframe):
    col = ['Item','Weight','Consumed','Wasted','Storage','Purchase_Date','Expiration_Date']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.success('Updated')
    
    
# ----- User add items to pantry ----- #

df =  load_the_spreadsheet(Pantry)

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
        



# ----- User add annotation to pantry ----- #
annotated = st.experimental_data_editor(df)
add_submitted = st.button("Confirm Edit")
if add_submitted:
         update_annotated_spreadsheet('Pantry',annotated) # update google sheet
else:
     st.write('Incorrect')

df =  load_the_spreadsheet(Pantry)





    
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
