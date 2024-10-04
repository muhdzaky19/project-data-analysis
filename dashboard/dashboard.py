import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='darkgrid')
plt.style.use('dark_background')
day_df = pd.read_csv("./dashboard/day.csv")
hour_df = pd.read_csv("./dashboard/hour.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.sidebar.header('Date Range Filter')
min_date = pd.to_datetime(day_df['dteday'].min())
max_date = pd.to_datetime(day_df['dteday'].max())

start_date, end_date = st.sidebar.date_input('Select Date Range', 
                                             [min_date, max_date], 
                                             min_value=min_date, 
                                             max_value=max_date)

filtered_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & 
                         (day_df['dteday'] <= pd.to_datetime(end_date))]


st.title('Bike Sharing Analysis Dashboard')


tab1, tab2, tab3, tab4 = st.tabs([
    "Impact of Season and Weather on Rentals", 
    "Rental Patterns Over the Year", 
    "Rental Patterns During Work Hours", 
    "Environmental Impact on Rentals"
])

with tab1:
    st.subheader('How does the season and weather affect bike rentals?')
    
    season_data = filtered_day_df.groupby(['season', 'yr'])['cnt'].sum().reset_index()
    
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    season_data['season'] = season_data['season'].map(season_mapping)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='season', y='cnt', hue='yr', data=season_data, palette='coolwarm', ax=ax)
    ax.set_title('Total Rentals by Season and Year', fontsize=16)
    ax.set_xlabel('Season', fontsize=12)
    ax.set_ylabel('Total Rentals', fontsize=12)
    st.pyplot(fig)
    
    weather_data = filtered_day_df.groupby(['weathersit', 'yr'])['cnt'].sum().reset_index()

    weather_mapping = {
        1: 'Clear, Few clouds, Partly cloudy',
        2: 'Mist, Cloudy, Broken clouds',
        3: 'Light Snow, Light Rain, Thunderstorm',
        4: 'Heavy Rain, Snow, Fog'
    }
    weather_data['weathersit'] = weather_data['weathersit'].map(weather_mapping)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='weathersit', y='cnt', hue='yr', data=weather_data, palette='viridis', ax=ax)
    ax.set_title('Total Rentals by Weather Condition and Year', fontsize=16)
    ax.set_xlabel('Weather Condition', fontsize=12)
    ax.set_ylabel('Total Rentals', fontsize=12)
    st.pyplot(fig)


with tab2:
    st.subheader('How does bike rental vary across months?')
    
    # Group data by month and year, then calculate the total rentals
    monthly_data = filtered_day_df.groupby(['mnth', 'yr'])['cnt'].sum().reset_index()

    # Line plot showing rental patterns across months
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='mnth', y='cnt', hue='yr', marker='o', data=monthly_data, palette='coolwarm', ax=ax)
    ax.set_title('Total Rentals by Month and Year', fontsize=16)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Total Rentals', fontsize=12)
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    st.pyplot(fig)

with tab3:
    st.subheader('How do bike rentals vary during work hours (morning and evening)?')

    hourly_data = hour_df.groupby(['hr', 'yr'])['cnt'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='hr', y='cnt', hue='yr', marker='o', data=hourly_data, palette='coolwarm', ax=ax)
    ax.axvspan(7, 9, color='orange', alpha=0.3, label='Morning Peak (7AM-9AM)')
    ax.axvspan(17, 19, color='green', alpha=0.3, label='Evening Peak (5PM-7PM)')
    ax.set_title('Average Rentals by Hour and Year', fontsize=16)
    ax.set_xlabel('Hour of Day', fontsize=12)
    ax.set_ylabel('Average Rentals', fontsize=12)
    plt.xticks(range(0, 24))
    st.pyplot(fig)

with tab4:
    st.subheader('How do environmental factors (Temperature, Humidity, Windspeed) affect bike rentals?')

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.regplot(x='temp', y='cnt', data=filtered_day_df, scatter_kws={'alpha':0.5}, line_kws={'color':'orange'}, ax=ax)
    ax.set_title('Impact of Temperature on Bike Rentals', fontsize=16)
    ax.set_xlabel('Temperature', fontsize=12)
    ax.set_ylabel('Average Rentals', fontsize=12)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.regplot(x='hum', y='cnt', data=filtered_day_df, scatter_kws={'alpha':0.5}, line_kws={'color':'blue'}, ax=ax)
    ax.set_title('Impact of Humidity on Bike Rentals', fontsize=16)
    ax.set_xlabel('Humidity', fontsize=12)
    ax.set_ylabel('Average Rentals', fontsize=12)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.regplot(x='windspeed', y='cnt', data=filtered_day_df, scatter_kws={'alpha':0.5}, line_kws={'color':'green'}, ax=ax)
    ax.set_title('Impact of Windspeed on Bike Rentals', fontsize=16)
    ax.set_xlabel('Windspeed', fontsize=12)
    ax.set_ylabel('Average Rentals', fontsize=12)
    st.pyplot(fig)
