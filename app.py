
import streamlit as st
import pathlib
import requests
url = "http://127.0.0.1:8002/add"

page_bg_image = """
<style>
[data-testid="stAppViewContainer"]{
    background-color: #40E0D0;
    background: linear-gradient(to right, #4A90E2, #50C878); /* Soft Blue to Mint Green Gradient */
    opacity: 0.9;
}

h1 {
    color: white !important;
}

h3 {
    color: white !important;
}

# .stTextInput, .stTextArea {
#     background-color: white;
#     color: black;
#     # border-radius: 1px;
# }

.stButton button {
    background-color: #008CBA;
    color: white;
    border-radius: 5px;
}

.stTextInput input, .stTextArea textarea {
    color: black;
}
</style>
"""
st.markdown(page_bg_image, unsafe_allow_html=True)

def save_user_data(username, password, email):

        
    data={
    
    'username':username,
    'password':password,
    'email':email
    }

    response=requests.post(url,json=data)

def signup():
    st.subheader("Please fill in the details below to create a new account.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    
    if st.button("Sign Up"):
        if username and password and email:
            save_user_data(username, password, email)
            st.success("User registered successfully!")
        else:
            st.error("Please fill in all fields.")

# Login page

def check_user_credentials(username, password,user):
    for use in user:
        if use[0]==username and use[1]==password:
            return True
    return False
    
def login():
    
    st.subheader("Enter your credentials to log in.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        urll ="http://127.0.0.1:8002/"
        response=requests.get(urll)
        if response.status_code==200:
            data=response.json()
            users=data['users']
        
            if check_user_credentials(username, password,users):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()  
            else:
                st.error("Incorrect username or password.")
        else:
            st.error('Unable to fetch data')


def home():
    st.title("Welcome to ChatSphere!")
    st.write(f"Hi, {st.session_state.username}! Welcome to the ChatSphere!")
    
    if st.button("Sign Out"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun() 

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.title("Welcome to ChatSphere!")
        st.write("Please login or register to continue.")
    
    if st.session_state.logged_in:
        home() 
    else:

        action = st.selectbox("Choose an option", ["Login", "Sign Up"])

        if action == "Sign Up":
            signup()
        elif action == "Login":
            login()

if __name__ == "__main__":
    main()
