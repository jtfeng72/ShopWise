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
#from datetime import datetime, date


@st.cache_data()
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
st.write(df.info())
#datetime.datedf["Purchase_Date"]
#df["P_Month"] = df["Purchase_Date"].dt.month

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
status = st.sidebar.multiselect(
    "Select your grocery status:",
    options=df["Status"].unique(),
    default=df["Status"].unique()               #prepopulate all status
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


