import streamlit as st
from groq import Groq
import time
import folium
from folium import plugins
import pandas as pd
from streamlit.components.v1 import html  # Import html function to render folium map

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Set up the title and description for the Streamlit app
st.set_page_config(page_title="Gaia: Women Safety App", page_icon="🤖", layout="centered")
st.title("Gaia: Women Safety App")
st.markdown("Gaia is an AI-powered app providing emotional support and real-time safety features for women.")

# Chat input section
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def get_response(user_input):
    """Get response from Groq AI model."""
    # Append user input to the conversation history
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # Call Groq API to get the AI's response
    chat_completion = client.chat.completions.create(
        messages=st.session_state['messages'],
        model="llama3-8b-8192"  # Specify model you want to use from Groq
    )
    
    # Get the response from the API and add it to the chat history
    ai_message = chat_completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": ai_message})
    
    return ai_message

# Sidebar for navigation
st.sidebar.title('Features')
page = st.sidebar.radio("Choose a feature", ["AI-Powered Support", "Emergency Call", "Dangerous Area Map"])

if page == "AI-Powered Support":
    st.header("Simulate a Call with Gaia AI")
    user_input = st.text_input("Tell Gaia how you're feeling:", "")

    if user_input:
        ai_response = get_response(user_input)
        st.markdown(f"**Gaia (AI):** {ai_response}")

elif page == "Emergency Call":
    st.header("Emergency Call Simulation")

    # Button to simulate calling emergency services
    emergency_button = st.button("Call Emergency Services")

    if emergency_button:
        # Simulating the emergency call (this could be replaced with real APIs like Twilio in the future)
        with st.spinner('Connecting to emergency services...'):
            time.sleep(2)  # Simulating a short delay
            st.success("Emergency services have been contacted. Help is on the way!")
            st.write("You will receive assistance shortly. Stay safe!")

elif page == "Dangerous Area Map":
    st.header("Dangerous Area Map (Prototype)")

    # Sample data for dangerous areas (latitude, longitude, and danger level)
    # In a real application, you would replace this with real-time data from APIs.
    data = {
        'latitude': [40.7128, 34.0522, 51.5074, 48.8566, 35.6762],
        'longitude': [-74.0060, -118.2437, -0.1278, 2.3522, 139.6503],
        'area': ['New York', 'Los Angeles', 'London', 'Paris', 'Tokyo'],
        'danger_level': ['High', 'Medium', 'Low', 'High', 'Medium']  # Danger levels (High, Medium, Low)
    }

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Create a folium map centered around the mean coordinates
    map_center = [df['latitude'].mean(), df['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=2)

    # Function to assign colors based on danger level
    def get_color(danger_level):
        if danger_level == 'High':
            return 'red'
        elif danger_level == 'Medium':
            return 'orange'
        else:
            return 'green'

    # Add markers for each dangerous area
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

    # Add a heatmap layer (optional) to visualize concentration of dangerous areas
    heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows()]
    plugins.HeatMap(heat_data).add_to(m)

    # Display the folium map in the Streamlit app
    st.subheader("Dangerous Areas Map")
    st.write("This map visualizes areas with different danger levels.")
    st.markdown("Use the color code to interpret the danger level:")
    st.markdown("🟥 High | 🟧 Medium | 🟩 Low")

    # Render the folium map in the Streamlit app using the html function
    map_html = m._repr_html_()  # Generate HTML representation of the folium map
    html(map_html, height=500)  # Use Streamlit's HTML rendering

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
