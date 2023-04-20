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
st.title('Pantry')


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
w = s.worksheet("DropBox")

values_list = w.col_values(3)

option = st.selectbox('Which pantry would you like to access?', (values_list))
st.write('You selected:', option)


# ----  Connect to the Google Sheet ---- 
sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
sheet_name = "Pantry_Loc_Line"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")


# --- Build a user interface and search functionality --- #
text_search = st.text_input("Search items by item description", value="")

m1 = df["Pantry_ID"].str.contains(text_search)
m2 = df["Storage"].str.contains(text_search)
df_search = df[m1 | m2]

if text_search:
    st.write(df_search)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
Catagory = st.sidebar.multiselect(
    "Select the Pantry_ID:",
    options=df["Pantry_ID"].unique(),
    default=df["Pantry_ID"].unique()
)

Name = st.sidebar.multiselect(
    "Select the Storage:",
    options=df["Storage"].unique(),
    default=df["Storage"].unique(),
)

df_selection = df.query(
    "Pantry_ID == @Pantry_ID & Storage ==@Storage"
)

st.dataframe(df_selection)

