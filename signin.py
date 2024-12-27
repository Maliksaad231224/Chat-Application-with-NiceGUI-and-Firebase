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

def get_image(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

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
            padding: 1rem; /* Increased padding */
            border-radius: 15px; /* More rounded corners */
            border: 2px solid #fff;
            width: 500px;
            max-width: 600px; /* Increased width */
            height: 500px;    /* Increased height */
            backdrop-filter: blur(8px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

        }}
     .login-title {{
            text-align: center;
            font-size: 2rem;  /* Increased font size */
            font-weight: 500;
            margin-bottom: 2rem;  /* Increased margin */
        }}

        .login-box {{
            display: flex;
            align-items: center;
            border-bottom: 2px solid #fff;
            padding-bottom: 5rem;
            width: 1rem;
            margin-bottom: 1.5rem;
        }}

        .login-box input {{
            width: 90%; /* Increased width */
            padding: 1rem; /* Increased padding */
            background: transparent;
            border: 1px solid #fff;
            border-radius: 5px;
            color: white;
            font-size: 1.1rem; /* Increased font size */
        }}

        .login-box label {{
            color: #fff;
            position: absolute;
            top: -1rem;
            left: 1rem;
            font-size: 1rem;
            transition: 0.3s ease-in-out;
        }}

        .login-eye {{
            position: absolute;
            right: 10px;
            top: 30%;
            cursor: pointer;
        }}

        .login-button {{
            background-color: #007bff;
            color: white;
            padding: 1rem;  /* Increased padding */
            width: 90%;     /* Increased width */
            border: none;
            border-radius: 5px;
            font-size: 1.2rem;  /* Increased font size */
            cursor: pointer;
            margin-top: 1.5rem; /* Increased margin */
        }}

        .register-text {{
            text-align: center;
            margin-top: 1.5rem;  /* Increased margin */
        }}
        .text-input-wrapper {{
            display: flex;
            align-items: center;
            width: 80%;
            margin-bottom: 10px;
            border: 2px solid #fff;
            border-radius: 25px;
            background-color: transparent;
            color:white;
       }}

        .text-input-wrapper img {{
            width: 20px;
            height: 20px;
            margin-left: 10px;
            color:white;
        }}
        .text-input username{{
            color = white;
        }}
        .text-input-wrapper input {{
            flex: 1;
            color:white;
            border: none;
            outline: none;
            padding-left: 10px;
            background-color: transparent;
            color: white;
            font-size: 1rem;
            border-radius: 25px;
        }}
    </style>
    """
    ui.add_head_html(page_bg_image)  # This adds the style to the page

# Sign Up page function

otp_storage = {}
def signup():
    set_background()  # Apply background styles

    # Center the form container in the middle of the page
    with ui.column().classes('login-form').style('text-align: center; ') as form_container:
        ui.label('Sign Up').style('color:white; font-size: 44px; text-align: center; background:none;')
       
        username = ui.input('Username').classes('text-input').style('''
            width: 80%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
        ''').props('label-color=cyan-8 clearable input-class=text-white')
        username.props('autocomplete=off') 
       

        # Password input with white text and background
        password = ui.input('Password').classes('text-input').style('''
            width: 80%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
            background-color: transparent;
        ''').props('label-color=cyan-8 clearable input-class=text-white')
        password.props('autocomplete=off ') 

        # Email input with white text and background
        email = ui.input('Email').classes('text-input').style('''
           width: 80%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
            background-color: transparent;
        ''')
        email.props('autocomplete=off') 
        
        send_otp_button = ui.button('Send OTP')
    
        async def handle_send_otp():
            if email.value:
                otp = generate_otp()
                result = await send_otp_email_async(email.value, otp)
                if result == True:
                    otp_storage[email.value] = otp
                # Only show OTP fields after email is sent
                    otp_digits = []
                    
                    ui.label('Enter the OTP sent to your email:').style('color:white;')
                    otp_input = ui.input().style(
                        '''
                                   width: 80%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
            background-color: transparent;
            ''')
                    otp_input.props('maxlength=6')
                    otp_input.props('maxlength=6 autocomplete=off inputmode=numeric')  
                # Sign up button that verifies OTP
                    sign_up_button = ui.button("Sign Up")

                    def handle_sign_up():
                        if len(otp_input) == 6 and otp_input == otp_storage[email.value]:
                            if username.value and password.value:
                                ui.label("User registered successfully!").style('color:white;')
                                #over here #
                            else:
                                ui.label("Please fill in all fields.").style('color:white;')
                        else:
                            ui.label("Incorrect OTP. Please try again.").style('color:white;')

                    sign_up_button.on_click(handle_sign_up)

                else:
                    ui.label(f"Error sending OTP: {result}").style('color:white;')
            else:
                ui.label("Please enter a valid email address.").style('color:white;')

        send_otp_button.on_click(handle_send_otp)  # Start the UI

signup()
ui.run(port=8001)