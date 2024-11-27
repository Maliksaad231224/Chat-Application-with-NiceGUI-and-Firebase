import random
import smtplib
from email.message import EmailMessage
import streamlit as st

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


st.title("OTP Email Verification")

email = st.text_input("Enter your email address:")

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

if "otp" in st.session_state:
    user_otp = st.text_input("Enter the OTP sent to your email:")

    if st.button("Verify OTP"):
        if user_otp == st.session_state["otp"]:
            st.success("OTP Verified!")
        else:
            st.error("Invalid OTP. Please try again.")
