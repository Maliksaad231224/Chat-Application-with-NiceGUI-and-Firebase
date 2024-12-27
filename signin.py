from nicegui import ui
import random
import smtplib
from email.message import EmailMessage
import asyncio
import base64
import os

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
            height: 100vh;
            margin: 0;
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
        </style>
    """
    ui.add_head_html(page_bg_image)

# Sign up page function
otp_storage = {}

def signup():
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
        ''').props('label-color=white clearable input-class=text-white')

        password = ui.input('Password', password=True, password_toggle_button=True).classes('text-input').style('''
            width: 80%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
            background-color: transparent;
        ''').props('label-color=white clearable input-class=text-white')

        email = ui.input('Email').classes('email-input').style('''
            width: 80%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
            background-color: transparent;
        ''').props('label-color=white clearable input-class=text-white')

        send_otp_button = ui.button('Send OTP').style('width:80%')

        # Predefine and hide OTP and result sections
        otp_section = ui.row().style('display: none')  # Hide OTP input section initially
        otp_input = ui.input('Enter OTP').props('maxlength=6 autocomplete=off inputmode=numeric label-color=white clearable input-class=text-white').style('''
            width: 80%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
            background-color: transparent;
        ''')
        otp_result_label = ui.label().style('color:white')

        # Predefine the sign-up button, but keep it hidden initially
        sign_up_button = ui.button('Sign Up').style('display: none; width:80%')
        otp_section.style('display: flex') 
        sign_up_button.style('display: block')  
        # Hide Sign-Up button initially

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
            if otp_input.value == otp_storage.get(email.value):
                if username.value and password.value:
                    otp_result_label.set_text("User registered successfully!")
                else:
                    otp_result_label.set_text("Please fill in all fields.")
            else:
                otp_result_label.set_text("Incorrect OTP. Please try again.")

        sign_up_button.on_click(handle_sign_up)

signup()
ui.run(port=8002)
