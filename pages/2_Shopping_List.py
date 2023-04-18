import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage
import gcsfs
import pandas as pd
from io import StringIO 
import requests
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import gspread 
from gspread_pandas import Spread,Client
from pysmiles import read_smiles
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame

st.set_page_config(page_title = "ShopWise app",
                   page_icon= "list-task")
st.title('Shopping list')

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
sheet_name = "Pantry"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
Pantry_df = pd.read_csv(url, dtype=str).fillna("")


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

# Load data from worksheets
what_sheets = worksheet_names()
#st.sidebar.write(what_sheets)
ws_choice = st.sidebar.radio('Available worksheets',what_sheets)

# Create a select box 
df = load_the_spreadsheet(ws_choice)

# Show the availibility as selection
select_Name = st.sidebar.selectbox('Food_List_Master',list(df['Name']))


add = st.sidebar.checkbox('Add New Item')
if add :  
    name_entry = st.sidebar.text_input('New Item')
    confirm_input = st.sidebar.button('Confirm')
    
    if confirm_input:
        now = datetime.now()
        opt = {'Name': [name_entry],
              'Time_stamp' :  [now]} 
        opt_df = DataFrame(opt)
        df = load_the_spreadsheet('Pantry')
        new_df = df.append(opt_df,ignore_index=True)
        update_the_spreadsheet('Pantry',new_df)

