#ShopWise Dashboard.py
# ----- Entire code below  ------- #  

# ----- Import libraries  ------- #  
import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage
import gcsfs
import pandas as pd
import requests
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import gspread 
from gspread_pandas import Spread,Client
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame

# ----- Page setup ----- #
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='wide')
st.title('Welcome to ShopWise')


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
def update_the_user_cell():
    sh.update('C5', username)
    st.sidebar.info('Updated to GoogleSheet')

with st.form("form"):
    username = st.text_input("Please enter your user name.")
    submitted = st.form_submit_button("Confirm")
    
    if submitted:
        update_the_user_cell()


# --- Get List Value and make drop down --- #
# open your spreadsheet
s = spread.open("ShopWise Food List") 
# and worksheet
w = s.worksheet("DropBox")


# Update to Shopping cell
def update_the_shopping_cell():
    wks.update('D7', shopping_option)
    st.sidebar.info('Updated to GoogleSheet')

with st.form("my_form"):
    shopping_values_list = w.col_values(1)
    shopping_option = st.selectbox('Which shopping list would you like to access?', (shopping_values_list))
    submitted = st.form_submit_button("Confirm")
    
    if submitted:
        update_the_shopping_cell()


# Update to Pantry cell
def update_the_pantry_cell():
    wks.update('D22', Pantry_option)
    st.sidebar.info('Updated to GoogleSheet')

with st.form("my_form_1"):
    Pantry_values_list = w.col_values(3)
    Pantry_option = st.selectbox('Which pantry location would you like to access?', (Pantry_values_list))
    submitted = st.form_submit_button("Confirm")
    
    if submitted:
        update_the_pantry_cell()



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
    col = ['Name','Time_stamp']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')





