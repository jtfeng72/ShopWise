#ShopWise Recommended Items.py
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
from datetime import date


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

dashboard = sh.worksheet("Dashboard V2")

sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
d_rec = "Dashboard_Rec"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={d_rec}"
dashr = pd.read_csv(url, dtype=str).fillna("")


# ----- Creating functions ----- #
## Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df

def update_the_status_cell():
    dashboard.update('T4', option)
    dashboard.update('V4', str(str_date))
    dashboard.update('W4', str(end_date))
    st.sidebar.info('Updated to GoogleSheet')


# ----- Rec Dashboard ----- #
st.markdown('Item Recomendation')

with st.form("form"):
    option = st.selectbox("Item Category?",('Meat', 'Dairy', 'Processed Agricultural Products', 'Non-Processed Agricultural Products', 'Seafood'))
    str_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    submitted = st.form_submit_button("Confirm")
    
    if submitted:
        update_the_status_cell()

dashr=load_the_spreadsheet(d_rec)

AgGrid(dashr)

v = dashboard.cell('S2').value
st.write(v)
