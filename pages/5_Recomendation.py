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
df_c=df.query('Status == "Completed"')

#get all avaliable food items from master list for drop down features
sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
fd_list_sheet = "Food_List_Master"
fd_list_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={fd_list_sheet}"
fd_list = pd.read_csv(fd_list_url, usecols = ['Name','Category','CO2_Per_g'])

#Merging df
df_c2= df_c.merge(fd_list,
                  left_on= 'Item',
                  right_on= 'Name',
                  how = 'left')
 
df_c2['Emission']= df_c2['Wasted'] * df_c2['CO2_Per_g']                     # Calculating Emission


#st.write(df.dtypes) #to check data type
df_c2["Purchase_Date"] = pd.to_datetime(df_c2["Purchase_Date"]).dt.strftime('%Y-%m-%d')                #change to datetime
df_c2["Month"] = pd.to_datetime(df_c2["Purchase_Date"]).dt.strftime('%B')                           #new column to extract month
df_c2["Year"] = pd.to_datetime(df_c2["Purchase_Date"]).dt.year                           #new column to extract month


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
year = st.sidebar.multiselect(
    "Filter by Year :",
    options=df_c2["Year"].unique(),
    default=df_c2["Year"].unique()               #prepopulate all status
)

month = st.sidebar.multiselect(
    "Filter by Month :",
    options=df_c2["Month"].unique(),
    default=df_c2["Month"].unique()               #prepopulate all status
)

df_selection = df_c2.query(
    "Year == @year & Month == @month" 
)

#adding new columns


st.title(':bar_chart: Here are your grocery stats') #Page Title
st.markdown("##")
total_waste = round(df_selection['Wasted'].sum()/1000,2)
total_emission = round(df_selection['Emission'].sum(),2)
left_column, right_column = st.columns(2)

with left_column:
    st.subheader(f"Total Waste: {total_waste:,} kg")
with right_column:
    st.subheader(f"Total Emissions: {total_emission:,} kgCO2eq")
    
st.markdown("""---""")

#st.dataframe(df_selection)

#---visualization---#
# emission by category
emis_by_cat = (
    df_selection.groupby(by=["Category"]).sum()[["Emission"]].sort_values(by="Emission")
)
fig_emis_by_cat = px.bar(
    emis_by_cat,
    x="Emission",
    y=emis_by_cat.index,
    orientation="h",
    title="<b>Waste Emission by Category</b>",
    color_discrete_sequence=["#0083B8"] * len(emis_by_cat),
    template="plotly_white",
)
fig_emis_by_cat.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# emission by month
emis_by_mth = (
    df_selection.groupby(by=["Month"]).sum()[["Emission"]]
)
fig_emis_by_mth = px.bar(
    emis_by_mth,
    x=emis_by_mth.index,
    y="Emission",
    orientation="v",
    title="<b>Waste Emission by Month</b>",
    color_discrete_sequence=["#0083B8"] * len(emis_by_mth),
    template="plotly_white",
)
fig_emis_by_mth.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#left_column, right_column = st.columns(2)
#left_column.plotly_chart(fig_emis_by_cat, use_container_width=True)
st.plotly_chart(fig_emis_by_cat, use_container_width=True)
st.plotly_chart(fig_emis_by_mth, use_container_width=True)
#right_column.plotly_chart(fig_product_sales, use_container_width=True)


