import random
import smtplib
from email.message import EmailMessage
from nicegui import ui

# Function to generate OTP
def generate_otp():
    otp = "".join([str(random.randint(0, 9)) for _ in range(6)])
    return otp

# Function to send OTP email
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

# Main UI code
def main():
    # Title
    ui.label("OTP Email Verification").style('font-size: 2em; color: #333;')

    # Input for email
    email = ui.input(placeholder="Enter your email address").style('width: 100%; max-width: 350px;')

    def send_otp_action():
        user_email = email.value
        if user_email:
            otp = generate_otp()
            result = send_otp_email(user_email, otp)
            if result == True:
                ui.notify("OTP has been sent to your email!", type='positive')
                ui.session.set("otp", otp)  # Store OTP in session
            else:
                ui.notify(f"Error sending OTP: {result}", type='negative')
        else:
            ui.notify("Please enter a valid email address.", type='warning')

    # Send OTP button
    ui.button("Send OTP", on_click=send_otp_action).style('margin-top: 20px; width: 35%; max-width: 350px;')

    # OTP verification section
    if "otp" in ui.session:
        user_otp = ui.input(placeholder="Enter the OTP sent to your email").style('width: 100%; max-width: 350px;')

        def verify_otp_action():
            if user_otp.value == ui.session["otp"]:
                ui.notify("OTP Verified!", type='positive')
            else:
                ui.notify("Invalid OTP. Please try again.", type='negative')

        # Verify OTP button
        ui.button("Verify OTP", on_click=verify_otp_action).style('margin-top: 20px; width: 35%; max-width: 350px;')

# Run the app
ui.page('/', main)
ui.run()
