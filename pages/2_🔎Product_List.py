# ShopWise.py

# ---- Import libraries ----

import streamlit as st 
import pandas as pd
from st_aggrid import AgGrid, JsCode, GridOptionsBuilder, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# ---- Page setup ---- 
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='wide')
st.title('🔎 Product List')

# ----  Connect to the Google Sheet ---- 
sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
sheet_name = "Food_List_Master"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
Category = st.sidebar.multiselect(
    "Select the Category:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

Name = st.sidebar.multiselect(
    "Select the Name:",
    options=df["Name"].unique(),
    default=df["Name"].unique(),
)

df_selection = df.query(
    "Category == @Category & Name ==@Name"
)

grid_options = {
    "columnDefs": [
        {
            "headerName": "Item Number",
            "field": "Item Number",
            "hide": True,
        },
        {
            "headerName": "Name",
            "field": "Name",
            "editable": True,
        },
        {
            "headerName": "CO2_Per_g",
            "field": "CO2_Per_g",
            "editable": True,
        },
        {
            "headerName": "Category",
            "field": "Category",
            "editable": True,
        },
                {
            "headerName": "Pantry",
            "field": "Pantry",
            "editable": True,
        },
        {
            "headerName": "Fridge",
            "field": "Fridge",
            "editable": True,
        },
        {
            "headerName": "Freezer",
            "field": "Freezer",
            "editable": True,
        },        
    ],
}

# ---- Build a user interface and search functionality ---- 
text_search = st.text_input("Search items by item description", value="")

m1 = df["Name"].str.contains(text_search)
m2 = df["Category"].str.contains(text_search)
df_search = df[m1 | m2]

if text_search:
    grid_return =(df_search, grid_options)


grid_return = AgGrid(df_selection, grid_options)
#new_df = grid_return["data"]

#st.write(new_df)
