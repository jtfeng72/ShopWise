# ----- Import Library ----- #
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
from gspread_pandas import Spread,Client
from pysmiles import read_smiles
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame
from collections import namedtuple
from streamlit_option_menu import option_menu
import altair as alt
import math
from PIL import Image
# ----- END ----- #


# ----- Page setup ----- #
#st.set_page_config(page_title = "Welcome to ShopWise app", layout= "centered")
st.title("Welcome to ShopWise app")

# ----- END ----- #
