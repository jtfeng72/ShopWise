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
from pprint import pprint
from googleapiclient import discovery

# ----- Page setup ----- #
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='wide')
st.title('Welcome to Pantry')

option = st.selectbox('Which pantry would you like to access?', ('Email', 'Home phone', 'Mobile phone'))
st.write('You selected:', option)


# ----- Disable certificate verification (Not necessary always) ----- #
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# --- Create a Google Authentication connection objectt --- #
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)

gc = gspread.authorize(credentials)
wks = gc.open("ShopWise Food List").sheet1



service = discovery.build('sheets', 'v4', credentials=credentials)

# The ID of the spreadsheet to retrieve data from.
spreadsheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"  # TODO: Update placeholder value.

# The A1 notation of the values to retrieve.
range_ = 'C2:C23'  # TODO: Update placeholder value.

# How values should be represented in the output.
# The default render option is ValueRenderOption.FORMATTED_VALUE.
value_render_option = ''  # TODO: Update placeholder value.


request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, valueRenderOption=value_render_option)
response = request.execute()

# TODO: Change code below to process the `response` dict:
st.write(response)
