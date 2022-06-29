import pandas as pd
import numpy as np
import time
import jinja2
import plotly.express as px  # pip install plotly-express
import plotly.figure_factory as ff
import streamlit as st  # pip install streamlit
import matplotlib.pyplot as plt
import pydeck as pdk
import io
from io import StringIO
import string

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO




st.set_page_config(page_title="Data Visualization on Amazon Data", page_icon=":bar_chart:", layout="wide")
st.header('NewYork Institute of Technology')
st.subheader('DTSC 630: Data Visualization - Final Project Presentation')
st.markdown('**Under the guidance of Professor Dr.Jerry Cheng**.')
st.text('Team members:\n 1.School ID: 1300836 - Kuldeep Malhotra  \n 2.School ID: 1303749 - Abhinav Sai Kanduri')

# page_bg_img = '''
# <style>
#       .stApp {
#   background-image: url("https://backiee.com/static/wpdb/wallpapers/1920x1080/287513.jpg");
#   background-size: cover;
# }
# </style>
# '''
# st.markdown(page_bg_img, unsafe_allow_html=True)

st.title(":bar_chart: Amazon Products Data from 2000 - 2014")
st.markdown("##")
#df = pd.read_csv("new_data_amazon.csv")

df_data = st.file_uploader("Browse the data to upload here",type=["csv","txt","xlsx"])
if df_data:
    if df_data.name[-3:] == "csv":
        df = pd.read_csv(df_data)
    elif df_data.name[-3:] == "txt":
        df = pd.read_csv(df_data)
    else:
        df = pd.read_excel(df_data)

    with st.spinner('Wait for it...'):
        time.sleep(3)
    st.success('Done!')

    st.dataframe(df)


    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='data.csv',
        mime='text/csv',
    )


# ---- SIDEBAR ----
    st.sidebar.header("Please filter the data here:")
    year = st.sidebar.multiselect(
        "Select the Year:",
        options=df["Year"].unique(),
        default=df["Year"].unique()
    )

    rating = st.sidebar.multiselect(
        "Select the Rating:",
        options=df["Rating"].unique(),
        default=df["Rating"].unique(),
    )

    state = st.sidebar.multiselect(
        "Select the State:",
        options=df["State"].unique(),
        default=df["State"].unique()
    )

    gender = st.sidebar.multiselect(
        "Select the Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

    price_choice = st.sidebar.slider(
        'Please select the Price USD :', min_value=100, max_value=5000, step=100, value=5000)



    df_selection = df.query("Year == @year & Rating==@rating  & State == @state & Gender == @gender | PriceUSD == @price_choice")



    ######## KPI's

    total_sales = int(df_selection["PriceUSD"].sum())
    average_rating = round(df_selection["Rating"].mean(), 1)
    star_rating = ":star:" * int(round(average_rating, 0))
    average_transaction = round(df_selection["PriceUSD"].mean(), 2)

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Price:")
        st.subheader(f"US $ {total_sales:,}")
    with middle_column:
        st.subheader("Average Rating:")
        st.subheader(f"{average_rating} {star_rating}")
    with right_column:
        st.subheader("Average Transaction:")
        st.subheader(f"US $ {average_transaction}")

    st.markdown("""---""")



    # line chart
    st.markdown('**line Chart**')
    my_bar = st.progress(0)

    for percent_complete in range(100):
         time.sleep(0.1)
         my_bar.progress(percent_complete + 1)
    linechart = pd.DataFrame(df_selection,columns=['Year', 'Rating' ])

    st.line_chart(linechart)



    # bar chart
    st.markdown('**Bar Chart**')
    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)
    st.balloons()
    chart_data = pd.DataFrame(df_selection, columns=['Rating', 'Year','Gender'])
    st.bar_chart(chart_data)




    # Add histogram data
    st.markdown('**Histogram**')
    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.1)
    my_bar.progress(percent_complete + 1)
    st.caption('Analysing the Ratings with in the range of year')
    st.snow()
    x1 = df_selection['Year']

    # Group data together
    hist_data = [x1]

    group_labels = ['Rating']

    # Create distplot with custom bin_size
    fig = ff.create_distplot(
             hist_data, group_labels, bin_size=[1, 1.25, 1.5])

    st.plotly_chart(fig, use_container_width=True)


    # Pie chart
    st.markdown('**Pie Chart**')
    st.caption('Showing the percentages of Rating with respect to the year')
    st.success('Showing the percentage of Rating and Year')
    labels = 'Ratings', 'Year'
    sizes = [15, 30]
    explode = (0.1, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)



    st.markdown('**Mapping the Location**')
    st.caption('generating random USA DATA with Latitude and Longitude')
    my_bar = st.progress(0)
    for percent_complete in range(100):
         time.sleep(0.1)
         my_bar.progress(percent_complete + 1)

    # generated data
    df = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [39, -86],
        columns=['lat', 'lon'])

    st.map(df)




    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)