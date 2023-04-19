#ShopWise.py
#---Import libraries---#
from collections import namedtuple
from streamlit_option_menu import option_menu
import altair as alt
import math
import pandas as pd
import streamlit as st
from PIL import Image
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder


#---Page setup---#
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='wide')
st.title('Shopping List')

#---Connect to the Google Sheet---#
sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
sheet_name = "Shopping_List2"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")

with st.form("form"):
    #with col1:
    purchase_dt = st.date_input("Date of Purchase")
    #with col2:
    item = st.selectbox('Food_List_Master',list(df['Name'])) 
    #with col3:
    weight = st.number_input("Weight(g)")
    #with col4:
    submitted = st.form_submit_button("Add Item")

