import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import time
import pandas as pd
import warnings
import folium

warnings.filterwarnings('ignore')

st.set_page_config(page_title='AirBnb_Analysis',page_icon=':barChart', layout = 'wide')

SELECT = option_menu(
    menu_title = None,
    options=['Home','Global Map','Street View','Explore Data'],
    #icons=['house','bar-chart','global'],
    default_index=1,
    orientation = "horizontal"
)

if SELECT == 'Home':
    st.header('Airbnb Analysis:')
    st.subheader('This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.')
    st.subheader('Domain:')
    st.subheader('Travel Industry, Property management and Tourism')
    
if SELECT == 'Global Map':
    st.subheader('Global Map of AirBnb Service')
    # Rename columns if needed
    df = pd.read_csv(r"D:\Data Sciene\Projects\My projects\Project 4\airbnb_data.csv")
    # Get unique countries
    countries_available = df['country'].unique()

    # Convert the array of countries to a comma-separated string
    countries_string = ', '.join(countries_available)

    # Display the list of countries horizontally
    st.write("<span style='font-size:16px'><b>List of Service available across countries:</b></span>", unsafe_allow_html=True)
    st.write(countries_string)
    
    # Add a checkbox to switch between viewing all data and filtered data
    view_filtered_data = st.checkbox("View filtered data by country")

    if view_filtered_data:
        # Add a filter to view by country using selectbox
        col1, col2, col3, col4= st.columns(4)
        with col1:
            selected_country = st.selectbox("Select country to view", countries_available)
            
        if st.button('Fetch Map View'):
            with st.spinner("Loading..."):
                time.sleep(2)
    
                # Filter DataFrame based on selected country
                filtered_df = df[df['country'].isin([selected_country])]  # Convert the selected country into a list

                # Rename columns if needed
                filtered_df = filtered_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

                # Display map for selected country
                st.map(filtered_df)
    else:
            # Display map for all data
            df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
            st.map(df)

if SELECT == 'Street View': 
    st.subheader("Select the country of street map view")
    df = pd.read_csv(r"D:\Data Sciene\Projects\My projects\Project 4\airbnb_data.csv")
    
    col1, col2, col3, col4= st.columns(4)
    with col1:
        group_country_data = st.selectbox('Select the Country', df['country'].unique())
    with col2: 
        group_street_data = st.selectbox("Pick the Street", df[df['country'] == group_country_data]["street"].unique())
    

    filtered_df = df[(df['country'] == group_country_data) & (df['street'] == group_street_data)]

    if st.button('Fetch Map View'):
        with st.spinner("Loading..."):
            time.sleep(2)
            filtered_df = filtered_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
            # Display map view using st.map
            st.map(filtered_df)
         
if SELECT == 'Explore Data':
    df = pd.read_csv(r"D:\Data Sciene\Projects\My projects\Project 4\airbnb_data.csv")
    st.markdown('Choose your filter:')
    
    col1, col2 = st.columns(2)
    with col1:
    # Create for country
        group_country_data = st.selectbox('Pick your Country', df['country'].unique())

    with col2:      
        # Create for street
        group_street_data = st.selectbox("Pick the Street", df[df['country'] == group_country_data]["street"].unique())
        
    filtered_df = df[(df['country'] == group_country_data) & (df['street'] == group_street_data)]
    

    col1, col2 = st.columns(2)
    with col1:
        pie_chart = px.pie(filtered_df, names='room_type', title='Room Type Distribution', color='room_type')

        # Update layout
        pie_chart.update_layout(
            title_font=dict(size=20),
            legend_title="Room Type", 
            legend_font=dict(size=14),
        )

        # Show the chart using Streamlit
        st.plotly_chart(pie_chart) 
        
    with col2:
        
        filtered_df = df[(df['country'] == group_country_data) & (df['street'] == group_street_data)]
        bar1 = px.bar(filtered_df, x='room_type',y='price',color='room_type')
        bar1.update_layout(title = 'Room type as per price',
                        title_font=dict(size=20),
                            xaxis=dict(title="Room Type", title_font=dict(size=20)),
                            yaxis=dict(title="Price", title_font=dict(size=20)))

        st.plotly_chart(bar1)
        
    col1, col2 = st.columns(2)
    with col1:
    # Create for country
        group_room_type = st.selectbox('Pick your Room Type', df['room_type'].unique())
        
        filtered_df = df[(df['country'] == group_country_data) & (df['street'] == group_street_data) & (df['room_type'] == group_room_type)]

        bar1 = px.bar(filtered_df, x='price',y='bed_type',color='room_type')
        bar1.update_layout(title = 'Room type as per price',
                        title_font=dict(size=20),
                            xaxis=dict(title="Room Type", title_font=dict(size=20)),
                            yaxis=dict(title="Price", title_font=dict(size=20)))

        st.plotly_chart(bar1)
        
    with col2:
    # Create for country
        group_bed_type = st.selectbox('Pick your bed_type', df['bed_type'].unique())
        
        filtered_df_GBT = df[(df['country'] == group_country_data) & (df['street'] == group_street_data) & (df['room_type'] == group_room_type) & (df['bed_type'] == group_bed_type)]

        bar1 = px.bar(filtered_df_GBT, x='price',y='bed_type',color='room_type')
        bar1.update_layout(title = 'Room type as per price',
                        title_font=dict(size=20),
                            xaxis=dict(title="Room Type", title_font=dict(size=20)),
                            yaxis=dict(title="Price", title_font=dict(size=20)))

        st.plotly_chart(bar1) 
        
    filtered_df = df[(df['country'] == group_country_data) & (df['street'] == group_street_data) & (df['room_type'] == group_room_type)]
    
    data1 = px.bar(filtered_df, x='host_name', y='price',color='host_name')
    data1.update_layout(title='Price per host',
                        title_font=dict(size=20),
                        xaxis=dict(title="Host Name", title_font=dict(size=20)),
                        yaxis=dict(title="Price", title_font=dict(size=20)))

    st.plotly_chart(data1, use_container_width=True)
     
    data1 = px.bar(filtered_df, x='host_name', y='availability_365',color='host_name')
    data1.update_layout(title='Availability of Host',
                        title_font=dict(size=20),
                        xaxis=dict(title="Host Name", title_font=dict(size=20)),
                        yaxis=dict(title="availability_365", title_font=dict(size=20)))

    st.plotly_chart(data1, use_container_width=True)
    
   
    data1 = px.bar(filtered_df, x='host_name', y='minimum_nights',color='host_name')
    data1.update_layout(title='minimum_nights',
                        title_font=dict(size=20),
                        xaxis=dict(title="Host Name", title_font=dict(size=20)),
                        yaxis=dict(title="minimum_nights", title_font=dict(size=20)))

    st.plotly_chart(data1, use_container_width=True)
    
    data1 = px.bar(filtered_df, x='host_name', y='bathrooms',color='host_name')
    data1.update_layout(title='Total no of Bathroom and Bedroom',
                        title_font=dict(size=20),
                        xaxis=dict(title="No of Bedroom", title_font=dict(size=20)),
                        yaxis=dict(title="No of Bathroom", title_font=dict(size=20)))

    st.plotly_chart(data1, use_container_width=True)
    

    data2 = px.bar(filtered_df, x='host_name', y='number_of_reviews',color='host_name')
    data2.update_layout(title='Rating as per Host',
                        title_font=dict(size=20),
                        xaxis=dict(title="Price", title_font=dict(size=20)),
                        yaxis=dict(title="No of reviews", title_font=dict(size=20)))

    st.plotly_chart(data2, use_container_width=True)
