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

#connection to the Shopping list table
sl_line_sheet = "Shopping_List_Line"
sl_line_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sl_line_sheet}"
sl_line_df = pd.read_csv(sl_line_url, dtype=str).fillna("")

#get all avaliable food items from master list for drop down features
fd_list_sheet = "Food_List_Master"
fd_list_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={fd_list_sheet}"
fd_list_df = pd.read_csv(fd_list_url, dtype=str).fillna("")


# --- Build a user interface and search functionality --- #
text_search = st.text_input("Search items by item description", value="")

m1 = sl_line_df["List_ID"].str.contains(text_search)
m2 = sl_line_df["Product_ID"].str.contains(text_search)
df_search = sl_line_df[m1 | m2] # filter column to have only List_ID and Product_ID

if text_search:
    st.write(df_search) #

with st.form("form"):
    purchase_dt = st.date_input("Date of Purchase")
    item = st.selectbox('Food Items', list(fd_list_df['Name'])) 
    weight = st.number_input("Weight(g)")
    submitted = st.form_submit_button("Add Item")

    if add_submitted:
         user_input_df=pd.DataFrame(columns = ['Purchase_dt', 'Items', 'Weight'])
         user_input = [purchase_dt,item, weight]
         user_input_df.loc[len(user_input_df.index)] = user_input # insert usert input

         for ind in user_input_df.index:
                  values_list = w.col_values(1)
                  length_row = len(values_list)
                  w.update_cell(length_row+1, 1, user_input_df['Purchase_dt'][ind])
                  w.update_cell(length_row+1, 2, str(user_input_df['Item'][ind]))
                  w.update_cell(length_row+1, 3, str(user_input_df['Weight'][ind]))
    

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:") #fillter table grocery store list name
s_list = st.sidebar.multiselect(
    "Select the List:",
    options=sl_name,
    default=sl_name
)

prod = st.sidebar.multiselect( #fillter table on proeduct ID
    "Select Product:",
    options=sl_line_df["Product_ID"].unique(),
    default=sl_line_df["Product_ID"].unique(),
)

s_list_ID = st.sidebar.multiselect( #fillter table grocery store list ID
    "Select List:",
    options=sl_ID,
    default=sl_ID,
)


df_selection = sl_line_df.query(
    "List_ID == @s_list_ID & Product_ID ==@prod"
)

st.dataframe(df_selection)
