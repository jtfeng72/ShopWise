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
url= "https://raw.githubusercontent.com/jtfeng72/ShopWise/master/Data/ShopWise%20Food%20List.csv"

st.write(df)
food_Item_dd = pd.read_csv(url)

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Name','Time_stamp']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')

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
