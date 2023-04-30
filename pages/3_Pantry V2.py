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
    df = pd.DataFrame(worksheet.get_all_records())
    return df

## Update add to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Item','Weight','Storage','Purchase_Date','Consumed','Done']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.success('Updated')

## Update annotated Sheet
def update_annotated_spreadsheet(spreadsheetname,dataframe):
    col = ['Item','Weight','Storage','Purchase_Date','Consumed','Done']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.success('Updated')

 #,'Wasted','Expiration','Expiration_Date'
    
# ----- User add items to pantry ----- #

df = load_the_spreadsheet(sheet_name)

with st.form("form"):
    st.header('Add items below')
    item = st.selectbox('Food Item (type to search/use dropdown)',list(fd_list_df['Name'])) 
    weight = st.number_input("Weight(g)")
    all_pantry = ["Pantry","Fridge","Freezer"]
    storage = st.selectbox("Select Storage Type",all_pantry) 
    purchase = st.date_input("Select Purchase Date")
    Consumed = st.number_input("Consumed(g)")
    Done = st.checkbox()
    add_submitted = st.form_submit_button("Add Item")
    
    if add_submitted:
        if len(df) == 0:
         user_input = {"Item": [item], "Weight": [weight], "Storage": [storage]
                      , "Purchase_Date": [purchase], "Consumed": [Consumed], "Done": [Done]} # User input dataframe
         user_input_df = pd.DataFrame(user_input)
         update_the_spreadsheet('Pantry',user_input_df) # update google sheet
         
        else:
         user_input = [item, weight,storage,purchase,Consumed,Done,"","",""] # User input dataframe
         df.loc[len(df.index)] = user_input # insert usert input
         update_the_spreadsheet('Pantry',df) # update google sheet
        

df = load_the_spreadsheet(sheet_name)

# ----- User add annotation to pantry ----- #

gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='multiple', use_checkbox=True)
gridoptions = gd.build()

grid_table = AgGrid(df, height=250, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED)

st.write('## Selected')
selected_row = grid_table["selected_rows"]
st.dataframe(selected_row)





annotated = st.experimental_data_editor(df)
add_submitted = st.button("Confirm Edit")

if add_submitted:
         update_annotated_spreadsheet('Pantry',annotated) # update google sheet
         df = load_the_spreadsheet(sheet_name) 
else:
     st.write('Incorrect')


df = load_the_spreadsheet(sheet_name)
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True,groupable=True)


