import streamlit as st
import requests
from fastapi import FastAPI, WebSocket, WebSocketException,Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
from pydantic import BaseModel
import uvicorn
import base64

# Function to get the image data in base64
def get_image(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Custom CSS for page background and container styles
def set_background():
    img = get_image(r'image\5053309.jpg')
    page_bg_image = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url('data:image/png;base64,{img}');
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
        opacity: 0.9;
        height: 100vh;
    }}
    h1, h3 {{
        color: white !important;
    }}
    .stButton button {{
        background-color: blue;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
    }}
    .stTextInput input {{
        color: black;
    }}
    .stTextArea textarea {{
        color: white;
        border: 1px solid #333;
        border-radius: 5px;
    }}
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
        color: white;
    }}
    p {{
        color: white !important;
        font-family: "Times New Roman", Times, serif;
        font-size: 1.3em;
    }}
    .stContainer {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100%;
        background: rgba(0, 0, 0, 0.7);
        border: 3px solid #0078D4; /* Border color updated */
        border-radius: 10px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Adding shadow for 3D effect */
    }}
    </style>
    """
    st.markdown(page_bg_image, unsafe_allow_html=True)


def check_user_credentials(username, password, users):
    for user in users:
        if user[0] == username and user[1] == password:
            return True
    return False

def login():
    set_background()  # Apply background and custom styling

    # Custom CSS for login form alignment
    st.markdown("""
    <style>
        /* Centering the container */
       .stApp {
            display: flex;
            justify-content: center;  /* Horizontally center the container */
            align-items: center;      /* Vertically center the container */
            height: 100vh;            /* Take up the full viewport height */
            flex-direction: column;   /* Stack items vertically */
        }

        /* Reduce the width of the input fields */
        .stTextInput, .stPassword, .stTextArea {
            width: 95%;  /* Set the width of the input container to 80% */
            max-width: 350px;  /* Maximum width to prevent it from becoming too wide */
            margin-bottom: 15px;  /* Add some space between the inputs */
        }

        .stTextInput input, .stPassword input, .stTextArea textarea {
            width: 100%;  /* Ensure the text input fills the container */
            padding: 10px;
            color:white;
        }

        /* Optional: Styling the button to match the centered inputs */
        .stButton button {
            width: 35%;
            max-width: 350px;
            margin-top: 20px;
             display: block;
             margin-left: auto;  /* Centers the button horizontally */
    margin-right: auto;  
        }
    </style>
    """, unsafe_allow_html=True)

    # Display the login form
    st.markdown("<h1 style='color:white; text-align:center;'>Welcome to Chat Sphere</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white; text-align:center;'>Login to Your Account</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])  # Centering the form
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Login button with centered text
        if st.button("Login"):
            urll = "http://127.0.0.1:8004/"
            response = requests.get(urll)
            if response.status_code == 200:
                data = response.json()
                users = data['users']

                if check_user_credentials(username, password, users):
                    st.success('Login successful')
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()  # Reload the app
                else:
                    st.error("Incorrect username or password.")
            else:
                st.error('Unable to fetch data')
