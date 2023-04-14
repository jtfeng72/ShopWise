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
import gcsfs
import pandas as pd
import requests
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

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

content = read_file(bucket_name, file_path)

#AgGrid(content)

#data = pd.read_csv(file_path,
                    #storage_options={'token' : credentials},
                    #low_memory=False,
                   # index_col=0)

# Print results.
#st.write(content)

d = {'Product_ID': [], 'Name': [], 'CO2eq_per_Kg': [],  'Catagory': [],  'Days_in_Pantry': [],  'Days_in_Fridge': [],  'Days_in_Freezer': []}

for line in content: # go through file line by line
    if line != '\n': # skip new line characters
        line = line.replace('\n', '') # get rid of '\n' in all fields
        key, val = line.split(',', 2) # take the first 2 tokens from the split statement
        d[key].append(val)

df = pd.DataFrame(d)

st.write(df)

    
#for line in content.strip().split("\n"):
   # Product_ID, Name , CO2eq_per_Kg , Catagory , Days_in_Pantry , Days_in_Fridge , Days_in_Freezer = line.split(",")
   # st.write(f"{Name} has a :{CO2eq_per_Kg}:")
    
#df = pd.read_csv('gs://shopwise-bucket/Food_List.csv')
#df = pd.DataFrame(content, columns = ['Product_ID','Name','CO2eq_per_Kg','Catagory','Days_in_Pantry','Days_in_Fridge','Days_in_Freezer'])
#AgGrid(df)

