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

st.title('🔖 Shopping List') #Page Title

# Disable certificate verification (Not necessary always)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# --- Create a Google Authentication connection objectt --- #
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)

client = Client(scope=scope,creds=credentials)
spreadsheetname = "ShopWise Food List"                #spreadsheet name
spread = Spread(spreadsheetname,client = client)      #load ShopWise Food List google sheet


# --- Call the spreadshet --- #
sh = client.open(spreadsheetname)                     #load ShopWise Food List google sheet
#worksheet_list = sh.worksheets()                      # list of ALL worksheets in the google sheet <Worksheet 'Shopping_List2' id:986753546>...

#get all avaliable food items from master list for drop down features
sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
fd_list_sheet = "Food_List_Master"
fd_list_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={fd_list_sheet}"
fd_list = pd.read_csv(fd_list_url, usecols = ['Name'])

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Item','Weight']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.success('Updated')

#Display the latest update
df = load_the_spreadsheet("Shopping_List2")


#---User input to add items--#

with st.form("form"):
    st.header('Add items below')
    item = st.selectbox('Food Item (type to search/use dropdown)',list(fd_list['Name'])) 
    weight = st.number_input("Weight(g)", min_value=0)
    add_submitted = st.form_submit_button("Add Item")
    
    with st.spinner('Processing...'):
             if add_submitted:
                 if weight == 0:
                           st.warning('You have 0 weight for your item', icon="⚠️")
                 elif len(df) == 0:
                  user_input = {"Item": [item], "Weight": [weight]} # User input dataframe
                  user_input_df = pd.DataFrame(user_input)
                  update_the_spreadsheet('Shopping_List2',user_input_df) # update google sheet

                 else:
                  user_input = [item, weight] # User input dataframe
                  df.loc[len(df.index)] = user_input # insert usert input
                  update_the_spreadsheet('Shopping_List2',df) # update google sheet
         

df = load_the_spreadsheet("Shopping_List2") #refresh google sheet
        
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True,groupable=True)

#  --- JavaScript function to add a new row to the AgGrid table ---         
js_del_row = JsCode ('''
function(e) {
 let api = e.api;
 let sel = api.getSelectedRows(); 
 api.applyTransaction({remove: sel}) 
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
                </style>
                <button id='click-button'
                    class="btn-danger"
                    > X </button>
            </span>
        `;
        }
        getGui() {
            return this.eGui;
        }
    };
    ''')         
    
gd.configure_selection(selection_mode= 'single')
gd.configure_column( field = 'Click to Remove', 
                     onCellClicked = js_del_row,      #adding delete function into the button
                     pre_selected_rows=[],
                     cellRenderer = cellRenderer_addButton, #adding the button desgin
                     lockPosition='left')
gridOptions = gd.build()


#---AG grid Remove item--#

with st.form('Shopping List') as f:
         st.header('Shopping List 🔖')
         '''If items are removed, Click "Confirm 🔒" to finalize the list below'''
         grid_table = AgGrid(df, 
                   gridOptions = gridOptions, 
                   fit_columns_on_grid_load = True,
                   theme = "streamlit",
                   allow_unsafe_jscode=True,
                   )
         st.info(f"Item/items in your shopping list: {len(grid_table['data'])}")
         submitted = st.form_submit_button("Confirm 🔒")
         
         with st.spinner('Processing...'):
                  if submitted:
                           df_final = grid_table["data"]
                           if df_final.empty:                                    #incase the ag-grid is cleared completely
                                    spread.clear_sheet(sheet = 'Shopping_List2')
                                    df_final = pd.DataFrame(columns=['Item','Weight'])
                                    update_the_spreadsheet('Shopping_List2',df_final) # update google sheet
                           else:
                                    spread.clear_sheet(sheet = 'Shopping_List2')
                                    update_the_spreadsheet('Shopping_List2',df_final) # update google sheet
