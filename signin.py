import streamlit as st
import requests
import base64
import login as lg
import random
import smtplib
from email.message import EmailMessage


def generate_otp():
    otp = "".join([str(random.randint(0, 9)) for _ in range(6)])
    return otp

def send_otp_email(to_email, otp):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        admin_mail = "moizulhaq331@gmail.com"
        passkey = "eqxm gzao hkze mfft" 
        server.login(admin_mail, passkey)

        msg = EmailMessage()
        msg["Subject"] = "OTP Verification"
        msg["From"] = "Admin of ChatSphere"
        msg["To"] = to_email
        msg.set_content(f"Your OTP is: {otp}")

        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return str(e)

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

def save_user_data(username, password, email):
    url = "http://127.0.0.1:8003/add"
    data = {
        'username': username,
        'password': password,
        'email': email
    }
    response = requests.post(url, json=data)
    return response.status_code == 200  # Return True if the user is saved successfully

def signup():
    set_background()
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
            width: 50%; /* Adjust the width of the button */
            max-width: 300px; /* Optional: Set a maximum width for the button */
            margin-top: 20px;
            display: block;
            margin-left: auto;  /* Centers the button horizontally */
            margin-right: auto;  
            padding: 10px 20px; /* Adjust the padding for better appearance */
            font-size: 16px; /* Adjust font size */
        }
            .stColumns {
            display: flex;
            color:white;
            justify-content: space-between;
            width: 100%;
        }
        .stColumns div {
            flex: 1;
            margin: 5px;
        }
    </style>
""", unsafe_allow_html=True)
# Create input fields
    st.markdown("""
    <h1 style='color:white; text-align:center;'>Welcome to the Chat Sphere</h1>
""", unsafe_allow_html=True)
    st.markdown("""
    <h3 style='color:white; text-align:center;'>Create a New Account</h3>
""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
       
        st.markdown("""
        <p style="text-align:center; color:white;">
            Already have an account? <a href="#" style="color:lightblue; text-decoration:none;" onclick="window.parent.postMessage({currentPage: 'login'}, '*')">Login</a>
        </p>
    """, unsafe_allow_html=True)
        if st.button("Send OTP"):
            if email:
                otp = generate_otp()
                result = send_otp_email(email, otp)

                if result == True:
                    st.success("OTP has been sent to your email!")
                    st.session_state["otp"] = otp
                else:
                    st.error(f"Error sending OTP: {result}")
            else:
                st.warning("Please enter a valid email address.")

       
        if 'otp' in st.session_state:
            st.markdown("<h3 style='color:white;'>Enter the OTP sent to your email:</h3>", unsafe_allow_html=True)

            # Display six OTP input boxes
            otp_digits = []
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1: 
                otp_digits.append(st.text_input("", max_chars=1, key="otp1"))
            with col2:
                otp_digits.append(st.text_input("", max_chars=1, key="otp2"))
            with col3:
                otp_digits.append(st.text_input("", max_chars=1, key="otp3"))
            with col4:
                otp_digits.append(st.text_input("", max_chars=1, key="otp4"))
            with col5:
                otp_digits.append(st.text_input("", max_chars=1, key="otp5"))
            with col6:
                otp_digits.append(st.text_input("", max_chars=1, key="otp6"))

            # Concatenate the OTP digits
            user_otp = "".join(otp_digits)

            # Submit the signup form and verify OTP
            if st.button("Sign Up", key='Signup_button'):
                if len(user_otp) == 6 and user_otp == st.session_state["otp"]:
                    # Check if the other fields are filled and sign up
                    if username and password:
                        if save_user_data(username, password, email):
                            st.success("User registered successfully!")
                        else:
                            st.error("Failed to register user.")
                    else:
                        st.error("Please fill in all fields.")
                else:
                    st.error("Incorrect OTP. Please try again.")