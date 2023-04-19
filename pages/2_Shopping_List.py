#ShopWise.py
#---Import libraries---#
from collections import namedtuple
from google.oauth2 import service_account
from gspread_pandas import Spread,Client
from streamlit_option_menu import option_menu
import altair as alt
import math
import pandas as pd
import streamlit as st
from PIL import Image
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder


# Disable certificate verification (Not necessary always)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# --- Create a Google Authentication connection objectt --- #
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "ShopWise Food List"
spread = Spread(spreadsheetname,client = client)

#st.write(spread.url)

# --- Call the spreadshet --- #
sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
sheet_name = "Shopping_List2"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
url2= "https://raw.githubusercontent.com/jtfeng72/ShopWise/master/Data/ShopWise%20Food%20List.csv"
sl_df = pd.read_csv(url, dtype=str).fillna("")

st.write(sl_df)
food_Item_dd = pd.read_csv(url2)

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Name','Time_stamp']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')

df = load_the_spreadsheet(sheet_name)

with st.form("form"):
    purchase_dt = st.date_input("Date of Purchase")
    item = st.selectbox('Food_List_Master',list(food_Item_dd['Name'])) 
    weight = st.number_input("Weight(g)")
    submitted = st.form_submit_button("Add Item")
    
    if submitted:
        opt = { "purchase_dt": [purchase_dt], "item": [item], "weight": [weight]}
        opt_df = pd.DataFrame(opt)
        df2 = load_the_spreadsheet('Pantry')
        new_df = df2.append(opt_df,ignore_index=True)
        update_the_spreadsheet('Shopping_List2',new_df)
        
        

    
#  --- Create a GridOptionsBuilder object from our DataFrame --- 
gd = GridOptionsBuilder.from_dataframe(df)

# Configure the default column to be editable
# sets the editable option to True for all columns
gd.configure_default_column(editable=True)


gridoptions = gd.build()


#  --- AgGrid Table with Button Feature --- 
# Streamlit Form helps from rerunning on every widget-click
# Also helps in providing layout

with st.form('Shopping List') as f:
    st.header('Shopping List 🔖')
    

    response = AgGrid(df,
                    gridOptions = gridoptions, 
                    editable=True,
                    allow_unsafe_jscode = True, 
                    theme = 'balham',
                    height = 200,
                    fit_columns_on_grid_load = True)
    st.write(" *Note: Don't forget to hit enter ↩ on new entry.*")
    st.form_submit_button("Confirm item(s) 🔒", type="primary")
