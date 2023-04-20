# ShopWise.py
# ----- Quick note --------#


# ----- Entire code below  ------- #

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

# ----- Page setup ----- #
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='wide')
st.title('Welcome to ShopWise')

# Disable certificate verification (Not necessary always)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# --- Create a Google Authentication connection objectt --- #

#---------------------------------------------------------
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)

gc = gspread.authorize(credentials)
wks = gc.open("ShopWise Food List").sheet1


# Update to user cell
def update_the_user_cell():
    wks.update('C5', username)
    st.sidebar.info('Updated to GoogleSheet')

with st.form("form"):
    username = st.text_input("Please enter your user name.")
    submitted = st.form_submit_button("Confirm")
    
    if submitted:
        update_the_user_cell()


# --- Get List Value and make drop down --- #
# open your spreadsheet
s = gc.open("ShopWise Food List") 
# and worksheet
w = s.worksheet("DropBox")


# Update to Shopping cell
def update_the_shopping_cell():
    wks.update('D7', shopping_option)
    st.sidebar.info('Updated to GoogleSheet')

with st.form():
    shopping_values_list = w.col_values(1)
    shopping_option = st.selectbox('Which shopping list would you like to access?', (shopping_values_list))
    submitted = st.form_submit_button("Confirm")
    
    if submitted:
        update_the_shopping_cell()


"""
#Pantry
pantry_values_list = w.col_values(3)
pantry_option = st.selectbox('Which pantry would you like to access?', (pantry_values_list))
st.write('You selected:', pantry_option)
"""









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





