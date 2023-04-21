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
st.title('Shopping List')
st.header('Add items below')


# ----- Disable certificate verification (Not necessary always) ----- #
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# --- Create a Google Authentication connection objectt --- #
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
gc = gspread.authorize(credentials)

# --- Get List Value and make drop down --- #
# open your spreadsheet
s = gc.open("ShopWise Food List") 
# and worksheet
w = s.worksheet("DropBox") #get data from dropbox tab

sl_name = w.col_values(1) #get data from dropbox 1st column (Shopping list)
sl_ID = w.col_values(2) #get data from dropbox 2st column (Shopping list ID)

option = st.selectbox('Which pantry would you like to access?', (sl_name))
st.write('You selected:', option)


# ----  Connect to the Google Sheet ---- 
sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
sheet_name = "Shopping_List_Line"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")


# --- Build a user interface and search functionality --- #
text_search = st.text_input("Search items by item description", value="")

m1 = df["List_ID"].str.contains(text_search)
m2 = df["Product_ID"].str.contains(text_search)
df_search = df[m1 | m2] # filter column to have only List_ID and Product_ID

if text_search:
    st.write(df_search) #

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
s_list = st.sidebar.multiselect(
    "Select the List:",
    options=sl_name,
    default=sl_name
)

prod = st.sidebar.multiselect(
    "Select Product:",
    options=df["Product_ID"].unique(),
    default=df["Product_ID"].unique(),
)

s_list_ID = st.sidebar.multiselect(
    "Select List:",
    options=sl_ID,
    default=sl_ID,
)


df_selection = df.query(
    "sl_ID == @s_list_ID & Product_ID ==@prod"
)

st.dataframe(df_selection)
