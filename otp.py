import random
import smtplib
from email.message import EmailMessage

class OTP_auth:

    def generate_otp():
         return random.randint(1000,9999)


    def send_otp_email(to_email, otp):
        msg = EmailMessage()
        msg.set_content(f"Your OTP for Banking System login is: {otp}")
        msg["Subject"] = "Banking System Login OTP"
        msg["From"] = "pratayayamritsharmayo@gmail.com"
        msg["To"] = to_email

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("pratayayamritsharmayo@gmail.com", "bxpaaxvwqzxnsqkd")
        server.send_message(msg)
        server.quit()
