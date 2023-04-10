# ShopWise.py
# Import libraries
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='wide')
st.title('Welcome to ShopWise')

# Connect to the Google Sheet

@set.cache
def get_dat_from_sheet():
    sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
    sheet_name = "Food_List_Master"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url, dtype=str).fillna("")
    return df

df = ger_data_from_sheet()
 
# Build a user interface and search functionality
text_search = st.text_input("Search items by item description", value="")

m1 = df["Name"].str.contains(text_search)
m2 = df["Catagory"].str.contains(text_search)
df_search = df[m1 | m2]

if text_search:
    st.write(df_search)
