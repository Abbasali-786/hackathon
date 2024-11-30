import streamlit as st
import requests
import time
import folium
from folium import plugins
import pandas as pd
from streamlit.components.v1 import html
from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Set up the title and description for the Streamlit app
st.set_page_config(page_title="Gaia: Women Safety App", page_icon="🤖", layout="centered")

# Function to get AI response (Groq model)
def get_response(user_input):
    """Get response from Groq AI model."""
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
        
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # Call Groq API to get the AI's response
    chat_completion = client.chat.completions.create(
        messages=st.session_state['messages'],
        model="llama3-8b-8192"  # Specify model you want to use from Groq
    )
    
    ai_message = chat_completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": ai_message})
    
    return ai_message

# Sidebar for navigation
st.sidebar.title('Features')
page = st.sidebar.radio("Choose a feature", ["Personal Information", "AI-Powered Support", "Emergency Call", "Dangerous Area Map", "ORS Route"])

# Personal Information Page (First Page)
if page == "Personal Information":
    st.title("Personal Information Page")
    st.write("Please fill in the following details:")
    
    with st.form(key='personal_info_form'):
        full_name = st.text_input("Full Name")
        country = st.text_input("Country")
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
        gender = st.radio("Gender", ('Male', 'Female', 'Other'))
        email = st.text_input("Email Address")
        phone_number = st.text_input("Phone Number")
        address = st.text_area("Address")
        
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.subheader("Your Personal Information:")
        st.write(f"**Full Name:** {full_name}")
        st.write(f"**Country:** {country}")
        st.write(f"**Age:** {age}")
        st.write(f"**Gender:** {gender}")
        st.write(f"**Email:** {email}")
        st.write(f"**Phone Number:** {phone_number}")
        st.write(f"**Address:** {address}")
        st.write("Thank you for sharing your details! You can now access the app's features.")

# AI-Powered Support Page
elif page == "AI-Powered Support":
    st.header("Simulate a Call with Gaia AI")
    user_input = st.text_input("Tell Gaia how you're feeling:", "")

    if user_input:
        ai_response = get_response(user_input)
        st.markdown(f"**Gaia (AI):** {ai_response}")

# Emergency Call Page
elif page == "Emergency Call":
    st.header("Emergency Call Simulation")

    emergency_button = st.button("Call Emergency Services")

    if emergency_button:
        with st.spinner('Connecting to emergency services...'):
            time.sleep(2)  # Simulating a short delay
            st.success("Emergency services have been contacted. Help is on the way!")
            st.write("You will receive assistance shortly. Stay safe!")

# Dangerous Area Map Page
elif page == "Dangerous Area Map":
    st.header("Dangerous Area Map (Prototype)")

    data = {
        'latitude': [40.7128, 34.0522, 51.5074, 48.8566, 35.6762],
        'longitude': [-74.0060, -118.2437, -0.1278, 2.3522, 139.6503],
        'area': ['New York', 'Los Angeles', 'London', 'Paris', 'Tokyo'],
        'danger_level': ['High', 'Medium', 'Low', 'High', 'Medium']
    }

    df = pd.DataFrame(data)
    map_center = [df['latitude'].mean(), df['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=2)

    def get_color(danger_level):
        if danger_level == 'High':
            return 'red'
        elif danger_level == 'Medium':
            return 'orange'
        else:
            return 'green'

    for index, row in df.iterrows():
        danger_color = get_color(row['danger_level'])
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=10,
            color=danger_color,
            fill=True,
            fill_color=danger_color,
            fill_opacity=0.7,
            popup=f"Area: {row['area']}<br> Danger Level: {row['danger_level']}"
        ).add_to(m)

    heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows()]
    plugins.HeatMap(heat_data).add_to(m)

    st.subheader("Dangerous Areas Map")
    st.write("This map visualizes areas with different danger levels.")
    st.markdown("Use the color code to interpret the danger level:")
    st.markdown("🟥 High | 🟧 Medium | 🟩 Low")

    map_html = m._repr_html_()
    html(map_html, height=500)

# ORS Route Page (New Page)
elif page == "ORS Route":
    st.title("OpenRouteService: Route Calculator")
    st.write("Enter your current location and destination to calculate the route:")

    # User inputs for current location and destination
    start_lat = st.number_input("Enter the latitude of the start point:", value=40.7128)
    start_lon = st.number_input("Enter the longitude of the start point:", value=-74.0060)
    end_lat = st.number_input("Enter the latitude of the destination:", value=34.0522)
    end_lon = st.number_input("Enter the longitude of the destination:", value=-118.2437)

    if st.button("Calculate Route"):
        if start_lat and start_lon and end_lat and end_lon:
            # OpenRouteService API key
            api_key = '5b3ce3597851110001cf6248678e77a7fc474afbbb5ec203d721079c'
            start_point = f'{start_lon},{start_lat}'  # ORS expects lon, lat
            end_point = f'{end_lon},{end_lat}'
            
            # API request to OpenRouteService
            url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_point}&end={end_point}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                # Extract the route information
                route = data['features'][0]['geometry']['coordinates']
                route_map = folium.Map(location=[start_lat, start_lon], zoom_start=12)

                # Plot the route on the map
                folium.PolyLine(locations=[(lat, lon) for lon, lat in route], color='blue', weight=5).add_to(route_map)

                # Display the route map in the app
                st.subheader("Calculated Route")
                route_html = route_map._repr_html_()
                html(route_html, height=500)
            else:
                st.error(f"Error: {response.status_code}")
        else:
            st.error("Please enter valid coordinates for both start and end locations.")

# Styling the chat window (Optional)
st.markdown("""
    <style>
    .css-1v3fvcr {
        font-family: 'Arial', sans-serif;
        background-color: #f0f2f6;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }
    .css-15zrgwt {
        font-size: 1.1rem;
        line-height: 1.5;
    }
    .css-10hldgk {
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)
