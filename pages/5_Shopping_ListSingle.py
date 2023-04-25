#ShopWise.py
#---Import libraries---#
from google.oauth2 import service_account
from gspread_pandas import Spread,Client
import pandas as pd
import streamlit as st
import gspread 
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.title('Shopping List')

