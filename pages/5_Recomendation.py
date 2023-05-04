#ShopWise.py
#---Import libraries---#
from google.oauth2 import service_account                      #pip install google-auth
from gspread_pandas import Spread,Client                       #pip install gspread_pandas
import pandas as pd                                            #pip install pandas
import streamlit as st                                         #pip install streamlit
from streamlit_option_menu import option_menu
import gspread                                                 #pip install gspread
from st_aggrid import AgGrid, GridUpdateMode, JsCode           #pip install streamlit-aggrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import plotly.express as px                                     #pip install plotly-express
from datetime import datetime, date


#@st.cache_data()
def load_the_spreadsheet(tabname):
    # --- Create a Google Authentication connection objectt --- #
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_info(
                    st.secrets["gcp_service_account"], scopes = scope)

    client = Client(scope=scope,creds=credentials)
    spreadsheetname = "ShopWise Food List"                #spreadsheet name
    #spread = Spread(spreadsheetname,client = client)      #load ShopWise Food List google sheet
    # --- Call the spreadshet --- #
    sh = client.open(spreadsheetname)                     #load ShopWise Food List google sheet
    #worksheet_list = sh.worksheets()                      # list of ALL worksheets in the google sheet <Worksheet 'Shopping_List2' id:986753546>...
    worksheet = sh.worksheet(tabname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df
df=load_the_spreadsheet("Pantry")
df_c=df.query('Status == "Completed"')
fd_list=load_the_spreadsheet("Food_List_Master")

#Merging df
df_c2= df_c.merge(fd_list,
                  left_on= 'Item',
                  right_on= 'Name',
                  how = 'left')
df_c3 = df_c2[["Item", "Category", "Weight", "Storage", "Purchase_Date","Consumed","Wasted","CO2_Per_g","Expiration","Expiration_Date"]]
 
df_c3['emission']= df_c3['Waste'] * df_c3['CO2_Per_g']


#st.write(df.dtypes) #to check data type
df_c3["Purchase_Date"] = pd.to_datetime(df["Purchase_Date"])               #change to datetime
df_c3["P_Month"] = df_c3["Purchase_Date"].dt.month                            #new column to extract month
df_c3["p_Year"] = df_c3["Purchase_Date"].dt.year                           #new column to extract month

#year to date parameter
ytd_start_date = pd.to_datetime(date(date.today().year, 1, 1))
ytd_end_date = pd.to_datetime(date.today())
ytd_flit=(df['Purchase_Date'] > ytd_start_date) & (df['Purchase_Date'] <= ytd_end_date)

st.dataframe(df_c3)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
status = st.sidebar.multiselect(
    "Select your grocery status:",
    options=df_c3["Status"].unique(),
    default=df_c3["Status"].unique()               #prepopulate all status
)

df_selection = df.query(
    "Status == @status"
)

#adding new columns
st.dataframe(df_selection)


st.title(':bar_chart: Here are your grocery stats') #Page Title
st.markdown("##")
total_waste = int(df_selection['Wasted'].sum())
left_column, right_column = st.columns(2)

with left_column:
    st.subheader(f"Total Waste: {total_waste:,} g")
#with right_column:
#    st.subheader(f"Total Waste: {total_emission:,} g")


