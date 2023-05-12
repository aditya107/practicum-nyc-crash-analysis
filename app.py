###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
######## Dev = Aditya
######## University = University at Buffalo
######## website = https://www.linkedin.com/in/aditya107/
######## status of project = Completed(more features to be added)
######## deployed = ##pending
######## Completed as a part of MS Practicum under Prof. Dominic Sellitto 
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

#DATA_URL=(
#"C:\Users\adide\OneDrive\Documents\MSPracticum\Motor_Vehicle_Collisions_-_Crashes.csv"

DATA_URL= st.file_uploader("Upload your NYC traffic data as a CSV file", type=["csv"])
# Set the title and description of the app
st.title("Motor Vehicle collisions in NYC")
st.markdown("This application is a Streamlit dashboard that can be used to "
"analyse motor vehicle collisions 🗽💥💥🚓"
"Completed for MSPracticum under Professor Dominic Sellitto.")
st.markdown(
    "<p style='text-align: center;'>Made by <a href='https://www.linkedin.com/in/aditya107/'>Aditya Singh</a></p>",
    unsafe_allow_html=True)

# Define a function to load the data and preprocess it
@st.cache(persist=True) # Add caching for faster reloads
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

# Load the data
data = load_data(167000)
# Making another copy of the data for future use
original_data = data

# Create a map to show where the most people are injured in NYC
st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of people injured in the collision", 1, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude","longitude"]].dropna(how="any"))

# Create a histogram to show how many collisions occur during a given hour of the day
st.header("How many collisions occur during a given time of the day?")
hour = st.slider("Hour to look at", 0, 23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehicle collision between %i:00 and %i:00" % (hour, hour + 1 % 24))
midpoint = (np.average(data['latitude']), np.average(data['longitude']))
st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
            "HexagonLayer",
            data = data[['date/time', 'latitude', 'longitude']],
            get_position = ['longitude', 'latitude'],
            radius = 100,
            extruded = True,
            pickable = True,
            elevation_scale = 4,
            elevation_range = [0, 1000],
            ),
        ]
))
# Create a bar chart to show the breakdown by minute between the chosen hour
st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour+1)% 24))
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour +1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60)) [0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
fig= px.bar(chart_data, x='minute', y = 'crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

st.header(" Top 5 unsafe streets for travel by affected type")
select = st.selectbox('Affected type of people', ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how='any')[:5])
elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how='any')[:5])
else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how='any')[:5])





if st.checkbox("Show Raw data", False):
    st.subheader('Raw Data')
    st.write(data)
