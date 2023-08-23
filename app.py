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
                    Welcome to the Superstore Sales with Streamlit app! This project aims to provide an easy-to-use interface for users to gain insights into sales trends, product performance, and customer behavior.
                    
                    ### [Tushar Aggarwal](https://tushar-aggarwal.com/)
                    """)


# File handler



    

#Progress  
@st.cache_data(ttl=600)  # Adjust ttl (time-to-live) as needed
def download_and_clean_data():
    # GitHub CSV file URL
    github_csv_url = 'https://raw.githubusercontent.com/tushar2704/Superstore-Sales-with-Streamlit/main/data_query/superstore.csv'

    # Fetch data from the GitHub URL
    response = requests.get(github_csv_url)

    if response.status_code == 200:
        # Read the CSV data into a Pandas DataFrame
        df = pd.read_csv(github_csv_url)
        return df
    else:
        return None
with st.spinner(text='Downloading & Cleaning Data'):
    df = download_and_clean_data()

# Check if the data is available and display it
if df is not None:
    pass
else:
    st.error("Failed to fetch data.")


main_navbar =option_menu(
    menu_title=None,
    options=['Home','Sales' ,'Sales by Time','Next', 'Time', '1', '2', '3'],
    icons=["house", "bar-chart-fill", "bar-chart-fill","bar-chart-fill","bar-chart-fill","bar-chart-fill","bar-chart-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal")


#2. compute top Analytics
df_selection= df.copy()
total_sales = float(df_selection['sales'].sum())
qty_sold = float(df_selection['quantity'].sum())
#  investment_mean = float(df_selection['Investment'].mean())
#  investment_median= float(df_selection['Investment'].median()) 
#  rating = float(df_selection['Rating'].sum())

 #3. columns
total1,total2,total3,total4,total5 = st.columns(5,gap='large')
with total1:
    st.info('Total Sales', icon="📶")
    
    st.metric(label = 'Total Sales', value= f"${total_sales:,.0f}")
    
    
# with total2:
# st.info('Most frequently', icon="🔍")
# st.metric(label='Mode TZS', value=f"{investment_mode:,.0f}")

# with total3:
# st.info('Investment Average', icon="🔍")
# st.metric(label= 'Mean TZS',value=f"{investment_mean:,.0f}")

# with total4:
# st.info('Investment Marging', icon="🔍")
# st.metric(label='Median TZS',value=f"{investment_median:,.0f}")

# with total5:
# st.info('Ratings', icon="🔍")
# st.metric(label='Rating',value=numerize(rating),help=f"""Total rating: {rating}""")

# st.markdown("""---""")





    







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


if main_navbar == "Home":
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
    








































































































