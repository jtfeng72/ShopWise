# ShopWise.py

# ---- Import libraries ----

import streamlit as st 
import pandas as pd
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# ---- Page setup ---- 
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='wide')
st.title('Welcome to ShopWise')

# ----  Connect to the Google Sheet ---- 
sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
sheet_name = "Food_List_Master"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")

# ---- Build a user interface and search functionality ---- 
text_search = st.text_input("Search items by item description", value="")

m1 = df["Name"].str.contains(text_search)
m2 = df["Catagory"].str.contains(text_search)
df_search = df[m1 | m2]

if text_search:
    st.write(df_search)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
Catagory = st.sidebar.multiselect(
    "Select the Catagory:",
    options=df["Catagory"].unique(),
    default=df["Catagory"].unique()
)

Name = st.sidebar.multiselect(
    "Select the Name:",
    options=df["Name"].unique(),
    default=df["Name"].unique(),
)

df_selection = df.query(
    "Catagory == @Catagory & Name ==@Name"
)

st.dataframe(df_selection)
