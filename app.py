#Superstore Sales with Streamlit
#© 2023 Tushar Aggarwal. All rights reserved. 
#https://github.com/tushar2704/



#Importing required Libraries
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')








#Page setups
#Application Title and Page Structure
#page config
st.set_page_config(page_title="Superstore Sales with Streamlit 🛒",
                   page_icon=":🛒:",
                   layout='wide')
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


#Page Title 
st.title("Superstore Sales with Streamlit")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


st.markdown("Welcome to the Superstore Sales with Streamlit app! This project aims to provide an easy-to-use interface for users to gain insights into sales trends, product performance, and customer behavior.")
st.markdown("""[Tushar-Aggarwal.com](https://tushar-aggarwal.com/)""")



#File handler



df = pd.read_excel(r"D:\Superstore-Sales-with-Streamlit\src\data\Superstore.xls")
#Date
col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting the min and max date 
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()


#Sidebars
st.sidebar.header("Choose your filter: ")
# Create for Region
region = st.sidebar.multiselect("Select Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]
    


# Create for State
state = st.sidebar.multiselect("Select State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]



















































































































