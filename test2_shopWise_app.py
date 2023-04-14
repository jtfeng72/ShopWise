# ShopWise.py
# ----- Quick note --------#


# ----- Entire code below  ------- #

import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage
import gcsfs
import pandas as pd
from io import StringIO 
import requests
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import gspread 

# ----- Page setup ----- #
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='wide')
st.title('Welcome to ShopWise')

# ----- Create API client ----- #
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# --- Connect to the Google Sheet --- 
sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
sheet_name = "Food_List_Master"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")




scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('coursera-362720-52b6aa46e070.json', scope)
client = gspread.authorize(creds)
 
sh = client.open('ShopWise Food List').worksheet('Food_List_Master')  
row = [Product_ID,Name,CO2eq_per_Kg,Catagory,Days_in_Pantry,Days_in_Fridge,Days_in_Freezer]
sh.append_row(row)







#  ----- Build a user interface and search functionality ----- #
text_search = st.text_input("Search items by item description", value="")

m1 = df["Name"].str.contains(text_search)
m2 = df["Catagory"].str.contains(text_search)
df_search = df[m1 | m2]

if text_search:
    st.write(df_search)


#  --- JavaScript function to add a new row to the AgGrid table --- 
js_add_row = JsCode ('''
function(e) {
 let api = e.api;
 let rowPos = e.rowIndex + 1; 
 api.applyTransaction({addIndex: rowPos, add: [{}]}) 
};
'''
)

#  --- Cell renderer for the '🔧' column to render a button --- 
cellRenderer_addButton = JsCode('''
    class BtnCellRenderer {
        init(params) {
            this.params = params;
            this.eGui = document.createElement('div');
            this.eGui.innerHTML = `
            <span>
                <style>
                .btn_add {
                    background-color: #71DC87;
                    border: 2px solid black;
                    color: #D05732;
                    text-align: center;
                    display: inline-block;
                    font-size: 12px;
                    font-weight: bold;
                    height: 2em;
                    width: 10em;
                    border-radius: 12px;
                    padding: 0px;
                }
                </style>
                <button id='click-button' 
                    class="btn_add" 
                    >&#x2193; Add</button>
            </span>
        `;
        }
        getGui() {
            return this.eGui;
        }
    };
    ''')

#  --- Create a GridOptionsBuilder object from our DataFrame --- 
gd = GridOptionsBuilder.from_dataframe(df)

# Configure the default column to be editable
# sets the editable option to True for all columns
gd.configure_default_column(editable=True)

# Configure the '🔧' column to use our the cell renderer 
# and onCellClicked function
gd.configure_column( field = '🔧', 
                     onCellClicked = js_add_row,
                     cellRenderer = cellRenderer_addButton,
                     lockPosition='left')

gridoptions = gd.build()


#  --- AgGrid Table with Button Feature --- 
# Streamlit Form helps from rerunning on every widget-click
# Also helps in providing layout

with st.form('Inventory') as f:
    st.header('Inventory List 🔖')
    
# Inside the form, we are displaying an AgGrid table using the AgGrid function. 
# The allow_unsafe_jscode parameter is set to True, 
# which allows us to use JavaScript code in the AgGrid configuration
# The theme parameter is set to 'balham', 
# which applies the Balham theme to the table
# The height parameter is set to 200, 
# which specifies the height of the table in pixels.
# The fit_columns_on_grid_load parameter is set to True, 
# which ensures that the columns of the table are resized to fit 
# the width of the table when it is first displayed

    response = AgGrid(df,
                    gridOptions = gridoptions, 
                    editable=True,
                    allow_unsafe_jscode = True, 
                    theme = 'balham',
                    height = 200,
                    fit_columns_on_grid_load = True)
    st.write(" *Note: Don't forget to hit enter ↩ on new entry.*")
    st.form_submit_button("Confirm item(s) 🔒", type="primary")
    
#  --- Visualize the AgGrid when submit button triggered ---#            
st.subheader("Updated Inventory")
# Fetch the data from the AgGrid Table
res = response['data']
st.table(res) 






