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

#  ----- Retrieve file contents into a DataFrame ----- #

bucket_name = "shopwise-bucket"
file_path = "Food_List.csv"

def read_csv_from_gcs(bucket_name, file_path):
  # Create a GCS client
  client = storage.Client(credentials=credentials)

  # Get the bucket and blob objects
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(file_path)

  # Download the contents of the blob as a string
  csv_data = blob.download_as_text()

  # Read the CSV data into a Pandas DataFrame
  dataframe = pd.read_csv(StringIO(csv_data))
  return dataframe

df = read_csv_from_gcs(bucket_name, file_path)

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
    
#  --- Visualize the AgGrid when submit button triggered ---            
st.subheader("Updated Inventory")
# Fetch the data from the AgGrid Table
res = response['data']
st.table(res) 


def send_to_database(res):
    # Create a list of scope values to pass to the credentials object
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    # Create a credentials object using the service account info and scope values
    credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
    
    # Authorize the connection to Google Sheets using the credentials object
    gc = gspread.authorize(credentials)
    
    # Open the Google Sheets document with the specified name
    sh = gc.open("AgGrid-Database")
    
    # Access the worksheet within the document with the specified name
    worksheet = sh.worksheet("Sheet1") 
    
    # Set up a progress bar
    my_bar = st.progress(0)
    
    # Iterate through the rows of the data frame
    for ind in res.index:
        # Calculate the percentage complete
        percent_complete = (ind+1)/len(res) 
        # Update the progress bar
        my_bar.progress(percent_complete)
        
        # Get the values in the first column of the worksheet
        values_list = worksheet.col_values(1)
        # Calculate the next empty row in the worksheet
        length_row = len(values_list)
        
        # Update the cells in the worksheet with the data from the data frame
        worksheet.update_cell(length_row+1, 1, res['Type'][ind])
        worksheet.update_cell(length_row+1, 2, str(res['Quantity'][ind]))
        worksheet.update_cell(length_row+1, 3, str(res['Price'][ind]))
       
    # Return a success message
    return st.success("Updated to Database ", icon="✅")\










