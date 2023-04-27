# ShopWise.py
#---Import libraries---#
from collections import namedtuple
from streamlit_option_menu import option_menu
import altair as alt
import math
import pandas as pd
import streamlit as st
from PIL import Image
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import streamlit as st


#---Page setup---#
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='wide')
st.title('Welcome to ShopWise')

# Display the Logo- Start---- -
image = Image.open('Shopwise_Logo.png')
st.image(image, caption='Shop Wisely')
# ----- END ----- #


#------Start- OF video-----#
video_file = open('Shopwise.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)
#-------End-------#
