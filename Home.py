import streamlit as st
import streamlit.components.v1 as components
import signin
import login

def set_custom_css():
    st.markdown("""
    <style>
        /* Change the background color of the button container */
        .navbar-container {
            background-color: #2C3E50;  /* Dark blue-gray background */
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Style the buttons */
        .navbar-container button {
            background-color: #3498DB;  /* Blue button color */
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Hover effect on buttons */
        .navbar-container button:hover {
            background-color: #2980B9;  /* Darker blue on hover */
        }
        
        /* Style the navbar header */
        .navbar-header {
            color: white !important;
            font-family: "Arial", sans-serif;
            font-size: 24px;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'
    
def navigate(page):
    st.session_state['current_page'] = page
def main():
    set_custom_css()
    
    if st.session_state['current_page'] == 'home':
        st.header("Welcome to the Chat Sphere!")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Home",key='home_but'):
                navigate('home')
        with col2:
            if st.button("Login",key='login_but'):
                navigate('login')
        with col3:
            if st.button("Signup",key='signup_but'):
                navigate('signup')
    elif st.session_state['current_page'] == 'login':
        login.login()
    elif st.session_state['current_page'] == 'signup':
        signin.signup()
if __name__ == "__main__":
    main()