import streamlit as st
import requests

def login():
        st.markdown("<div style='background-color: #f0f0f0; padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
        con = st.container(border=True)

        con.subheader("Enter your credentials to log in.")
        username = con.text_input("Username")
        password = con.text_input("Password", type="password")

        if con.button("Login"):
            urll = "http://127.0.0.1:8002/"
            response = requests.get(urll)
            if response.status_code == 200:
                data = response.json()
                users = data['users']

               
                con.session_state.logged_in = True
                con.session_state.username = username
                con.rerun()
            else:
                con.error("Incorrect username or password.")
        else:
            con.error('Unable to fetch data')
        con.markdown("</div>", unsafe_allow_html=True)
            
login()