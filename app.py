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
from streamlit_option_menu import option_menu
import requests
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

     
st.sidebar.markdown("""
                    ### Welcome to the Superstore Sales with Streamlit app! This project aims to provide an easy-to-use interface for users to gain insights into sales trends, product performance, and customer behavior.
                    
                    ### [Tushar Aggarwal](https://tushar-aggarwal.com/)
                    """)


# File handler

# @st.cache_data(ttl=600)
# def load_data(sheets_url):
#     csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
#     return pd.read_excel(csv_url)

# df = load_data(st.secrets["public_gsheets_url"])

#df=pd.read_csv(r'data_query\superstore.csv')
#df = pd.read_excel("src\data\Superstore.xls")
#, encoding='ISO-8859-1',on_bad_lines='skip'


# import psycopg2

# # Initialize connection.
# # Uses st.cache_resource to only run once.
# @st.cache_resource
# def init_connection():
#     return psycopg2.connect(**st.secrets["postgres"])

# conn = init_connection()

# # Perform query.
# # Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()

# rows = run_query("SELECT * from superstore;")

# # Print results.
# for row in rows:
#     st.write(f"{row[0]} has a :{row[1]}:")



#


# GitHub CSV file URL
github_csv_url = 'https://raw.githubusercontent.com/tushar2704/Superstore-Sales-with-Streamlit/main/data_query/superstore.csv'

# Fetch data from the GitHub URL
response = requests.get(github_csv_url)

if response.status_code == 200:
    # Read the CSV data into a Pandas DataFrame
    df = pd.read_csv(github_csv_url)
    
else:
    pass

#NavBar


# st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

# st.markdown("""
# <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #B6B7B2;">
#   <a class="navbar-brand" href="https://tushar-aggarwal.com/" target="_blank">Tushar Aggarwal</a>
#   <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
#     <span class="navbar-toggler-icon"></span>
#   </button>
#   <div class="collapse navbar-collapse" id="navbarNav">
#     <ul class="navbar-nav">
#       <li class="nav-item active">
#         <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="https://www.linkedin.com/in/tusharaggarwalinseec/" target="_blank">LinkedIn</a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="https://github.com/tushar2704" target="_blank">Github</a>
#       </li>
#     </ul>
#   </div>
# </nav>
# """, unsafe_allow_html=True)


#df = pd.read_excel(r"D:\Superstore-Sales-with-Streamlit\src\data\Superstore.xls")


main_navbar =option_menu(
    menu_title=None,
    options=['Home','Sales' ,'Sales by Time','Next', 'Time', '1', '2', '3'],
    icons=["house", "bar-chart-fill", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal")


if main_navbar == "Home":
    st.write("1")





    







#Sales by Date
col1, col2= st.columns((2))
df["order_date"] = pd.to_datetime(df["order_date"])

# Getting the min and max date 
startDate = pd.to_datetime(df["order_date"]).min()
endDate = pd.to_datetime(df["order_date"]).max()

with col1:
    date1 = pd.to_datetime(st.sidebar.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.sidebar.date_input("End Date", endDate))

df = df[(df["order_date"] >= date1) & (df["order_date"] <= date2)].copy()



# navbar_2=option_menu(
#     menu_title=None,
#     options=['Region', "---" ,'Sales', "---" ,'Sales by Time'],
#     icons=["house", "book", "envelope"],
#     menu_icon="cast",
#     default_index=0,
#     orientation="horizontal")

#Sidebars

# Create for Region

region = st.sidebar.multiselect("Select Region", df["region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["region"].isin(region)]
    


# Create for State
state = st.sidebar.multiselect("Select State", df2["state"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["state"].isin(state)]
    
    
# Create for City
city = st.sidebar.multiselect("Pick the City",df3["city"].unique())


# Filter the data based on Region, State and City

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["state"].isin(state)]
elif state and city:
    filtered_df = df3[df["state"].isin(state) & df3["city"].isin(city)]
elif region and city:
    filtered_df = df3[df["region"].isin(region) & df3["city"].isin(city)]
elif region and state:
    filtered_df = df3[df["region"].isin(region) & df3["state"].isin(state)]
elif city:
    filtered_df = df3[df3["city"].isin(city)]
else:
    filtered_df = df3[df3["region"].isin(region) & df3["state"].isin(state) & df3["city"].isin(city)]
 
 #Navigation for Salesbydate
category_df = filtered_df.groupby(by = ["category"], as_index = False)["sales"].sum()
cl1, cl2 = st.columns((2))
if main_navbar == "Sales":
    with col1:
        st.subheader("Category wise Sales")
        fig = px.bar(category_df, x = "category", y = "sales", text = ['${:,.2f}'.format(x) for x in category_df["sales"]],
                    template = "seaborn")
        st.plotly_chart(fig,use_container_width=True, height = 200)
 
    with col2:
        st.subheader("Region wise Sales")
        fig = px.pie(filtered_df, values = "sales", names = "region", hole = 0.5)
        fig.update_traces(text = filtered_df["region"], textposition = "outside")
        st.plotly_chart(fig,use_container_width=True)
    
    with cl1:
        with st.expander("Category_ViewData"):
            st.write(category_df)
            csv = category_df.to_csv(index = False).encode('utf-8')
            st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                                help = 'Click here to download the data as a CSV file')

    with cl2:
        with st.expander("Region_ViewData"):
            region = filtered_df.groupby(by = "region", as_index = False)["sales"].sum()
            st.write(region)
            csv = region.to_csv(index = False).encode('utf-8')
            st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')




if main_navbar == "Sales by Time":
    #Linechart
    filtered_df["month_year"] = filtered_df["order_date"].dt.to_period("M")
    st.subheader('Time Series Analysis')

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["sales"].sum()).reset_index()
    fig2 = px.line(linechart, x = "month_year", y="sales", labels = {"Sales": "Amount"},height=500, width = 1000,template="gridon")
    st.plotly_chart(fig2,use_container_width=True)

    with st.expander("View Data of TimeSeries:"):
        st.write(linechart.T)
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')

    #Treemap
    # Create a treem based on Region, category, sub-Category
    st.subheader("Hierarchical view of Sales using TreeMap")
    fig3 = px.treemap(filtered_df, path = ["region","category","sub_category"], values = "sales",hover_data = ["sales"],
                    color = "sub_category")
    fig3.update_layout(width = 800, height = 650)
    st.plotly_chart(fig3, use_container_width=True)
    
chart1, chart2 = st.columns((2)) 
 
if main_navbar == "Next":
#Piecharts

    with chart1:
        st.subheader('Segment wise Sales')
        fig = px.pie(filtered_df, values = "sales", names = "segment", template = "plotly_dark")
        fig.update_traces(text = filtered_df["segment"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    with chart2:
        st.subheader('Category wise Sales')
        fig = px.pie(filtered_df, values = "sales", names = "category", template = "gridon")
        fig.update_traces(text = filtered_df["category"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    import plotly.figure_factory as ff
    st.subheader(":point_right: Month wise Sub-Category Sales Summary")
    with st.expander("Summary_Table"):
        df_sample = df[0:5][["region","state","city","category","sales","profit","quantity"]]
        fig = ff.create_table(df_sample, colorscale = "Cividis")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("Month wise sub-Category Table")
        filtered_df["month"] = filtered_df["order_date"].dt.month_name()
        sub_category_Year = pd.pivot_table(data = filtered_df, values = "sales", index = ["sub_category"],columns = "month")
        st.write(sub_category_Year)

    # Create a scatter plot
    data1 = px.scatter(filtered_df, x = "sales", y = "profit", size = "quantity")
    data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                        titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                        yaxis = dict(title = "Profit", titlefont = dict(size=19)))
    st.plotly_chart(data1,use_container_width=True)

    with st.expander("View Data"):
        st.write(filtered_df.iloc[:500,1:20:2])

    # Download orginal DataSet
    csv = df.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")









































































































