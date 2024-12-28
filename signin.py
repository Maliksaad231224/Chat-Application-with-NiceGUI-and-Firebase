from nicegui import ui
import random
import smtplib
import firebase_admin
from firebase_admin import credentials, firestore, auth, db
from email.message import EmailMessage
import asyncio
import base64
import os


cred = credentials.Certificate('web-chat-app-b37b1-firebase-adminsdk-jiq57-6e131301e2.json')  # Path to your service account key
firebase_admin.initialize_app(cred)

def send_to_firebase(email, password):
    try:
        # Create a user with the provided email and password
        user = auth.create_user(
            email=email,
            password=password
        )
        print(f"Successfully created user: {user.uid}")
        return True  # Successfully created user
    except Exception as e:
        print(f"Error creating user: {e}")
        return e  # Failure to create user
# OTP generation function
def generate_otp():
    otp = "".join([str(random.randint(0, 9)) for _ in range(6)])
    return otp

# Send OTP email function
async def send_otp_email_async(to_email, otp):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        admin_mail = "moizulhaq331@gmail.com"
        passkey = "eqxm gzao hkze mfft"
        await asyncio.to_thread(server.login, admin_mail, passkey)

        msg = EmailMessage()
        msg["Subject"] = "OTP Verification"
        msg["From"] = "Admin of ChatSphere"
        msg["To"] = to_email
        msg.set_content(f"Your OTP is: {otp}")

        await asyncio.to_thread(server.send_message, msg)
        server.quit()
        return True
    except Exception as e:
        return str(e)

# Set background
def set_background():
    image_path = 'image/login-bg.png'
    if os.path.exists(image_path):
        ui.image(image_path).style("position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;")
    else:
        print("Error: Image not found at the specified path")
    
    page_bg_image = f"""
        <style>
        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, rgba(19, 23, 51, 0.8), rgba(0, 22, 58, 0.9));
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            animation: animateBg 5s infinite; 
            height: 100vh;
            margin: 0;
        }}
button {{
    background-color: transparent;
    color: white;
    border: 2px solid white;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

button:hover {{
    background-color: rgba(255, 255, 255, 0.1);
    transform: scale(1.05);
}}

button:active {{
    transform: scale(0.98);
}}
        .login-form {{
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 15px;
            border: 2px solid #fff;
            width: 500px;
            max-width: 600px;
            height: 600px;
            backdrop-filter: blur(8px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .text-input-wrapper input {{
            color: white;
            background-color: transparent;
        }}
        @keyframes animateBg {{
            100% {{
                filter: hue-rotate(30deg);  /* Corrected filter property */
            }}
        }}
        </style>
    """
    ui.add_head_html(page_bg_image)

# Sign up page function
otp_storage = {}

def signup_page():
    set_background()

    # Create form container
    with ui.column().classes('login-form').style('text-align: center; ') as form_container:
        ui.label('Sign Up').style('color:white; font-size: 44px; text-align: center; background:none;')
        
        username = ui.input('Username').classes('text-input').style('''
            width: 80%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: black;
            
        ''').props('label-color=white clearable input-class=text-white autocomplete=off spellcheck=false')

        password = ui.input('Password', password=True, password_toggle_button=True).classes('text-input').style('''
            width: 80%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
            background-color: transparent;
        ''').props('label-color=white clearable input-class=text-white autocomplete=off spellcheck=false')
        email = ui.input('Email').classes('email-input').style('''
            width: 80%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
            background-color: transparent;
        ''').props('label-color=white clearable input-class=text-white autocomplete=off spellcheck=false')
        send_otp_button = ui.button('Send OTP').classes('otp')

        # Predefine and hide OTP and result sections
        otp_section = ui.row().style('display: none')  # Hide OTP input section initially
        otp_input = ui.input('Enter OTP').props('maxlength=6 autocomplete=off inputmode=numeric label-color=white clearable input-class=text-white').style('''
            width: 80%;
            margin-bottom: 10px;
            padding-left:10px;
            filter: none !important;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
            background-color: transparent;
        
        ''')
        otp_result_label = ui.label().style('color:white')


        sign_up_button = None
        login_button = None
        otp_section.style('display: flex')   
        
        with ui.row().style('width: 100%; display: flex; justify-content: center; gap: 20px;'):
            sign_up_button = ui.button('Sign Up').classes('custom-button')
            login_button = ui.button('Login').classes('custom-button')
        ui.add_head_html("""
    <style>
        .custom-button {
               width: 38%;  /* Decreased width */
        background-color: transparent;
        color: white;
        border: 2px solid white;
        padding: 8px 16px;  /* Decreased padding for smaller height */
        border-radius: 25px;
        cursor: pointer;
        font-size: 14px;  /* Slightly smaller font */
        transition: background-color 0.3s ease, transform 0.2s ease;
    }
        .otp{
               width: 80%;  /* Decreased width */
        background-color: transparent;
        color: white;
        border: 2px solid white;
        padding: 8px 16px;  /* Decreased padding for smaller height */
        border-radius: 25px;
        cursor: pointer;
        font-size: 14px;  /* Slightly smaller font */
        transition: background-color 0.3s ease, transform 0.2s ease;
        }

      
   @keyframes animateCursor {
                0% {
                    transform: scale(1);
                }
                50% {
                    transform: scale(1.2);
                }
                100% {
                    transform: scale(1);
                }
            }
            
        .otp:hover {
            background-color: rgba255, 255, 255, 0.1);
            transform: scale(1.05);
            cursor: pointer;
            animation: animateCursor 0.5s ease-in-out infinite;
        }       
        .custom-button:hover {
            background-color: rgba255, 255, 255, 0.1);
            transform: scale(1.05);
            cursor: pointer;
            animation: animateCursor 0.5s ease-in-out infinite;
        }

        .text-input:hover {
            transform: scale(0.98);
            cursor: pointer;
            animation: animateCursor 0.5s ease-in-out infinite;
    </style>
""")


        async def handle_send_otp():
            if email.value:
                otp = generate_otp()
                result = await send_otp_email_async(email.value, otp)
                if result == True:
                    otp_storage[email.value] = otp
                    
                else:
                    otp_result_label.set_text(f"Error sending OTP: {result}")
            else:
                otp_result_label.set_text("Please enter a valid email address.")

        send_otp_button.on_click(handle_send_otp)


        def handle_sign_up():
            success=False
            if otp_input.value == otp_storage.get(email.value):
                if username.value and password.value:
                    otp_result_label.set_text("User registered successfully!")
                    success=send_to_firebase(email.value,password.value)
                    if success:
                        otp_result_label.set_text("User registered successfully!")
                    else:
                        otp_result_label.set_text(f"Error: {success}")
                else:
                    otp_result_label.set_text("Please fill in all fields.")
            else:
                otp_result_label.set_text("Incorrect OTP. Please try again.")

       
        sign_up_button.on_click(handle_sign_up)
        login_button.on_click(lambda: ui.run_javascript('window.location.href = "/login"'))

