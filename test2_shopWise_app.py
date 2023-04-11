# ShopWise.py
# ----- Quick note --------#
# Refer to YouTube video explaination - https://youtu.be/sOFM334iILs
# This gist was created for the purpose of embedding over the blog post.
# It is based on the original source code here - 
# https://github.com/avrabyt/YouTube-Tutorials/blob/main/Streamlit-Python/Streamlit-AgGrid-Usage/pages/aggrid-button-app.py
# An app is live based on the above repo , please refer to the live demo app here for testing - 
# https://avra-youtube-aggrid.streamlit.app/aggrid-button-app

# ----- Entire code below  ------- #

# Importing the dependencies
pip install streamlit-aggrid

import streamlit as st 
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.shared import JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Creates a Streamlit header and an Expander 
# to provide some context for the app.

st.header("AgGrid Demo `Part 3`")
with st.expander('🤩 What I plan to demonstrate today ? ', expanded=False):
    st.markdown('''
                
                ◻ 1. Implementing `button` within AgGrid table
                
                ◻ 2. Display any `update` made from the user-end
                
                ◻ 3. `Download` the AgGrid table
                
                ◻ 4. `Connect` to Database
                ''')

# Create an AgGrid table from a pandas DataFrame
d = {'Type':['Notebook', 'DVDs'] ,'Quantity': [1, 2],'Price': [400, 200]}
df = pd.DataFrame(data = d)
# Display the Dataframe in AgGrid
AgGrid(df)

# JavaScript function to add a new row to the AgGrid table
js_add_row = JsCode("""
function(e) {
    let api = e.api;
    let rowPos = e.rowIndex + 1; 
    api.applyTransaction({addIndex: rowPos, add: [{}]})    
};
"""     
)

# Cell renderer for the '🔧' column to render a button

# Resources to refer:
# https://blog.ag-grid.com/cell-renderers-in-ag-grid-every-different-flavour/
# https://www.w3schools.com/css/css3_buttons.asp

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

# Create a GridOptionsBuilder object from our DataFrame
gd = GridOptionsBuilder.from_dataframe(df)

# Configure the default column to be editable
# sets the editable option to True for all columns
gd.configure_default_column(editable=True)

# Configure the '🔧' column to use our the cell renderer 
# and onCellClicked function
gd.configure_column( field = '🔧', 
                     onCellClicked = js_add_row,
                     cellRenderer = cellRenderer_addButton
                    )
gridoptions = gd.build()

# AgGrid Table with Button Feature
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

# Visualize the AgGrid when submit button triggered           
st.subheader("Updated Inventory")
# Fetch the data from the AgGrid Table
res = response['data']
st.table(res)

# Plotting the data
st.subheader("Visualize Inventory")
st.bar_chart(data=res, x = 'Type', y = 'Price')

# Importing the necessary Library
from google.oauth2 import service_account
import gspread 

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

# If the "Send to Database" button is clicked, execute the send_to_database() function
col2.write("Save in Shared Cloud?")
if col2.button("Send to Database"):
    send_to_database(res)
