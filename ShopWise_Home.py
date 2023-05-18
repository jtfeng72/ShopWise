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


#---Start of Page setup---#
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='centered')
st.title('Welcome to ShopWise')
#---End of Page setup---#

st.write("Made by Kevin Luu, Kevin Feng, Andy Sun")
st.write("Welcome to ShopWise, your one-stop-shop for all things green and sustainable! Our app is designed to make eco-friendly shopping easier and more accessible than ever before, by wisely recommending a sustainable ammount to purchase. We understand that it can be overwhelming to navigate the world of green shopping, which is why we've curated a selection of products that meet our high standards for sustainability. With ShopWise, you can trust that every purchase you make is making a positive impact on the environment. We believe that small choices can make a big difference, and we're excited to help you make those choices every day. So join us in our mission to create a healthier planet, one shopping trip at a time. Download ShopWise today and start shopping with purpose!")

#------Start- OF video-----#
video_file = open('ShopWise Introduction.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)
#------End OF video--------#

#------------Start of Guides-----------#
st.title('Guide on how to use ShopWise')
#Shopping List
st.write("Guide for Shopping List  [link](https://scribehow.com/shared/ShopWise_shopping_list__Q-qGouGYQxSeTSAqA_okuA)")
#Pantry
st.write("Guide for Pantry  [link](https://scribehow.com/shared/Shopwise_Pantry__obEbbjM0S-6e_6f_3hEm4g)")
#Product List
st.write("Guide for Product List  [link](https://scribehow.com/shared/ShopWise_Product_List__E3FiloBgT7uH11ro1qc9cg)")
#Emission Metrics
st.write("Guide for Emission Metrics  [link](https://scribehow.com/shared/ShopWise_Emission_Metrics__aJ477AlcSUC2TmONVQWgHQ)")
#Item Recommendation
st.write("Guide for Item Recommendation  [link](https://scribehow.com/shared/ShopWise_Item_Recommendation__-r0GZF_YScOJ8lbwlf3ftA)")
#------------End of Guides-----------#
