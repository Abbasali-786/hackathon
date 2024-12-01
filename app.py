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

# Data preparation for London boroughs
data = {
    'borough': [
        'Barking and Dagenham', 'Barnet', 'Bexley', 'Brent', 'Bromley', 'Camden', 'Croydon', 'Ealing', 'Enfield', 
        'Greenwich', 'Hackney', 'Hammersmith and Fulham', 'Haringey', 'Harrow', 'Havering', 'Hillingdon', 'Hounslow', 
        'Islington', 'Kensington and Chelsea', 'Kingston upon Thames', 'Lambeth', 'Lewisham', 'Merton', 'Newham', 
        'Redbridge', 'Richmond upon Thames', 'Southwark', 'Sutton', 'Tower Hamlets', 'Waltham Forest', 'Wandsworth', 'Westminster'
    ],
    'total_crimes': [
        41254, 56255, 33090, 63128, 47102, 80824, 68039, 62115, 58731, 55079, 64607, 42676, 58046, 31539, 41315, 52754, 
        53224, 58236, 45477, 23418, 72894, 59341, 27779, 76691, 48207, 23918, 75450, 26231, 71909, 47295, 52018, 179016
    ],
    'safety_score': [
        0.789969551, 0.703949217, 0.83678443, 0.664537327, 0.756435326, 0.563063037, 0.636376148, 0.67034618, 0.689751074, 
        0.710692762, 0.656056288, 0.781815367, 0.693679074, 0.84567834, 0.789619758, 0.724025025, 0.7213299, 0.692589556, 
        0.765753574, 0.892246644, 0.608536089, 0.686253147, 0.867239333, 0.586762927, 0.750098917, 0.889379491, 0.593879201, 
        0.876116039, 0.614184381, 0.755328604, 0.728245474, 0
    ],
    'coordinates': [
        (51.5362, 0.0792), (51.625, -0.2062), (51.4572, 0.1492), (51.5588, -0.2817), (51.405, 0.0147), (51.545, -0.1628),
        (51.3721, -0.1004), (51.513, -0.3089), (51.6538, -0.0794), (51.4821, 0.0048), (51.545, -0.0557), (51.4927, -0.2339), 
        (51.5908, -0.1097), (51.5782, -0.3336), (51.5908, 0.1839), (51.5336, -0.458), (51.4712, -0.3662), (51.538, -0.103),
        (51.4975, -0.1903), (51.4123, -0.3007), (51.4576, -0.1158), (51.4452, -0.0209), (51.4146, -0.194), (51.5071, 0.0354), 
        (51.5588, 0.0824), (51.4479, -0.326), (51.5035, -0.081), (51.3618, -0.1944), (51.5173, -0.0416), (51.5908, -0.0118),
        (51.4576, -0.1924), (51.4975, -0.1372)
    ]
}

# Convert the data to a pandas DataFrame for easy manipulation
df = pd.DataFrame(data)

# Function to get AI response (Groq model)
def get_response(user_input):
    """Get response from Groq AI model."""
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # Call Groq API to get the AI's response
    chat_completion = client.chat.completions.create(
        messages=st.session_state['messages'],
        model="gemma2-9b-it"
    )
    
    ai_message = chat_completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": ai_message})
    
    return ai_message

# Sidebar for navigation
st.sidebar.title('Features')
page = st.sidebar.radio("Choose a feature", ["Personal Information", "AI-Powered Support", "Emergency Call", "London Crime Map", "ORS Route"])

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

# London Crime Map Page (Replaced Dangerous Area Map)
elif page == "London Crime Map":
    st.title("London Crime Map: Safe vs Dangerous Zones")
    
    # Create a map centered on London
    map_center = [51.5074, -0.1278]  # Coordinates of London
    crime_map = folium.Map(location=map_center, zoom_start=10)
    
    # Add markers for each borough, color-coded based on safety score
    for idx, row in df.iterrows():
        safety_score = row['safety_score']
        coords = row['coordinates']
        borough_name = row['borough']
        
        # Determine color based on safety score (green for safe, red for dangerous)
        if safety_score > 0.75:
            color = 'green'
        elif safety_score > 0.5:
            color = 'orange'
        else:
            color = 'red'
        
        folium.Marker(
            location=coords,
            popup=f"{borough_name}: {safety_score:.2f}",
            icon=folium.Icon(color=color)
        ).add_to(crime_map)
    
    # Display the map in Streamlit
    st.subheader("Map of London Boroughs: Safe and Dangerous Zones")
    st.write("Safe zones are marked in green, dangerous zones are marked in red.")
    st.components.v1.html(crime_map._repr_html_(), width=700, height=500)

# ORS Route Page (Route from one borough to another)
elif page == "ORS Route":
    st.title("OpenRouteService: Route Calculator between Boroughs")
    
    # Select start and end boroughs from the list
    boroughs = df['borough'].tolist()
    start_borough = st.selectbox("Select the start borough", boroughs)
    end_borough = st.selectbox("Select the destination borough", boroughs)
    
    if start_borough and end_borough:
        start_coords = df[df['borough'] == start_borough]['coordinates'].values[0]
        end_coords = df[df['borough'] == end_borough]['coordinates'].values[0]
        
        # OpenRouteService API key
        api_key = '5b3ce3597851110001cf6248678e77a7fc474afbbb5ec203d721079c'
        start_point = f'{start_coords[1]},{start_coords[0]}'  # ORS expects lon, lat
        end_point = f'{end_coords[1]},{end_coords[0]}'
        
        # API request to OpenRouteService
        url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_point}&end={end_point}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Extract the route information
            route = data['features'][0]['geometry']['coordinates']
            route_map = folium.Map(location=[start_coords[0], start_coords[1]], zoom_start=12)
    
            # Plot the route on the map
            folium.PolyLine(locations=[(lat, lon) for lon, lat in route], color='blue', weight=5).add_to(route_map)
    
            # Add markers for both start and end boroughs with safety color
            start_safety_score = df[df['borough'] == start_borough]['safety_score'].values[0]
            end_safety_score = df[df['borough'] == end_borough]['safety_score'].values[0]
            start_color = 'green' if start_safety_score > 0.75 else 'orange' if start_safety_score > 0.5 else 'red'
            end_color = 'green' if end_safety_score > 0.75 else 'orange' if end_safety_score > 0.5 else 'red'
            
            folium.Marker(
                location=start_coords,
                popup=f"{start_borough}: {start_safety_score:.2f}",
                icon=folium.Icon(color=start_color)
            ).add_to(route_map)
            
            folium.Marker(
                location=end_coords,
                popup=f"{end_borough}: {end_safety_score:.2f}",
                icon=folium.Icon(color=end_color)
            ).add_to(route_map)
    
            # Display the route map in the app
            st.subheader(f"Calculated Route from {start_borough} to {end_borough}")
            route_html = route_map._repr_html_()
            st.components.v1.html(route_html, width=700, height=500)
        else:
            st.error(f"Error: {response.status_code}")
