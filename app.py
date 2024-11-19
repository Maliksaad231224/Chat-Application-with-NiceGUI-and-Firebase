import streamlit as st
import pathlib
import requests
import base64

def get_image(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_image(r'image\5053309.jpg')
url = "http://127.0.0.1:8001/add"

# Custom CSS for page background and container styles
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

# Function to save user data
def save_user_data(username, password, email):
    data = {
        'username': username,
        'password': password,
        'email': email
    }
    response = requests.post(url, json=data)

con = st.container(border=True)
def signup():
        
        con.subheader("Please fill in the details below to create a new account.")
        username = con.text_input("Username")
        password = con.text_input("Password", type="password")
        email = con.text_input("Email")

        if con.button("Sign Up"):
            if username and password and email:
                save_user_data(username, password, email)
                con.success("User registered successfully!")
            else:
                con.error("Please fill in all fields.")

# Function to check user credentials
def check_user_credentials(username, password, users):
    for use in users:
        if use[0] == username and use[1] == password:
            return True
    return False

# Function for the login page
def chat():
    prompt:str=st.chat_input('Enter your message')
    user='name'
    assistant='assistant'
    if prompt:
        st.chat_message(user).write(prompt)
        st.chat_message(assistant).write('{user}:{prompt}')
def login():

        con.subheader("Enter your credentials to log in.")
        username = con.text_input("Username")
        password = con.text_input("Password", type="password")

        if con.button("Login"):
            urll = "http://127.0.0.1:8001/"
            response = requests.get(urll)
            if response.status_code == 200:
                data = response.json()
                users = data['users']

                if check_user_credentials(username, password, users):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    con.error("Incorrect username or password.")
            else:
                con.error('Unable to fetch data')
            chat()

def home():

        con.title("Welcome to ChatSphere!")
        con.write(f"Hi, {con.session_state.username}! Welcome to the ChatSphere!")
    
        if con.button("Sign Out"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    with con.container():
        if not st.session_state.logged_in:
            con.markdown("<h1 style='text-align: center; color:white; '>Welcome to ChatSphere!</h1>", unsafe_allow_html=True)
            con.write("<h3 style='text-align: center; color:white; '>Please login or register to continue.</h3>",unsafe_allow_html=True)
            action = con.selectbox("Choose an option", ["Login", "Sign Up"])
            if action == "Sign Up":
                signup()
            elif action == "Login":
                login()
            else:
                home()

# Run the app
if __name__ == "__main__":
    main()
