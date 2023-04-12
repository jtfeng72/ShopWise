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

content = read_file(bucket_name, file_path)

# Print results.
for line in content.strip().split("\n"):
    name, pet = line.split(",")
    st.write(f"{name} has a :{pet}:")

