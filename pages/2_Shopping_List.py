import streamlit as st
from google.oauth2 import service_account
import gspread

with st.form("form"):
    purchase_dt = st.date_input("Date of Purchase")
    item = st.selectbox('Food_List_Master',list(food_Item_dd['Name'])) 
    weight = st.number_input("Weight(g)")
    add_submitted = st.form_submit_button("Add Item")
    
    if add_submitted:
        user_input = { "Purchase_dt": [purchase_dt], "Item": [item], "Weight": [weight]} # User input dataframe
        user_input_df = pd.DataFrame(user_input)

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_info(
                        st.secrets["gcp_service_account"], scopes = scope)

        gc = gspread.authorize(credentials)
        s = gc.open("ShopWise Food List") 
        w = s.worksheet("Shopping_List2") #get data from dropbox tab
        for ind in user_input_df.index:
            values_list = worksheet.col_values(1)
            length_row = len(values_list)
            w.update_cell(length_row+1, 1, user_input_df['purchase_dt'][ind])
            w.update_cell(length_row+1, 2, str(user_input_df['item'][ind]))
            w.update_cell(length_row+1, 3, str(user_input_df['weight'][ind]))
      
