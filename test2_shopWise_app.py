# ShopWise.py
# ----- Quick note --------#
# Refer to YouTube video explaination - https://youtu.be/sOFM334iILs
# This gist was created for the purpose of embedding over the blog post.
# It is based on the original source code here - 
# https://github.com/avrabyt/YouTube-Tutorials/blob/main/Streamlit-Python/Streamlit-AgGrid-Usage/pages/aggrid-button-app.py
# An app is live based on the above repo , please refer to the live demo app here for testing - 
# https://avra-youtube-aggrid.streamlit.app/aggrid-button-app

# ----- Entire code below  ------- #

import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# Retrieve file contents.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    return content

bucket_name = "shopwise-bucket"
file_path = "Food_List.csv"

df = read_file(bucket_name, file_path)



# --- Build a user interface and search functionality --- 
#text_search = st.text_input("Search items by item description", value="")

#m1 = df["Name"].str.contains(text_search)
#m2 = df["Catagory"].str.contains(text_search)
#df_search = df[m1 | m2]

#if text_search:
    #st.write(df_search)


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


# Plotting the data
st.subheader("Visualize Inventory")
st.bar_chart(data=res, x = 'Name', y = 'Days_in_Pantry')

