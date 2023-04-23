import json
from datetime import datetime
import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
         st.secrets["gcp_service_account"], scopes = scope)
gc = gspread.authorize(credentials)
s = gc.open("ShopWise Food List") 
w = s.worksheet("Shopping_List2") #get data from dropbox tab

with st.form("form"):
    purchase_dt = st.date_input("Date of Purchase")
    item = st.text_input("Food Items") 
    weight = st.number_input("Weight(g)")
    add_submitted = st.form_submit_button("Add Item")
    
    if add_submitted:
        user_input = { "Purchase_dt": json.dumps(purchase_dt, default = str), "Item": [item], "Weight": [weight]} # User input dataframe
        user_input_df = pd.DataFrame(user_input)
        user_input_df['Purchase_dt']=datetime.strptime(user_input_df['Purchase_dt'], "%Y-%m-%d").strftime("%d-%m-%Y")

        for ind in user_input_df.index:
            values_list = w.col_values(1)
            length_row = len(values_list)
            w.update_cell(length_row+1, 1, user_input_df['Purchase_dt'][ind])
            w.update_cell(length_row+1, 2, str(user_input_df['Item'][ind]))
            w.update_cell(length_row+1, 3, str(user_input_df['Weight'][ind]))
      
