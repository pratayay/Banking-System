import db
import users
from otp import OTP_auth

current_user_id=None

class Authentication(users.User):

    def authenticate_ui(user_id, aadhar, mobile):
        global current_user_id
        try:
            db.cur.execute(
                """
                SELECT user_id
                FROM users
                WHERE user_id=%s AND aadhar=%s AND mobile=%s
                """,
                (user_id, aadhar, mobile)
            )
            data = db.cur.fetchone()

            if data:
                current_user_id = data[0]
                return True
            return False

        except Exception:
            return False

    
    def user_validation():
        global current_user_id
        try:
            print("*******User Authentication*********")
            user_id = int(input("Enter User ID: "))
            mobile_no = input("Enter Mobile Number: ")

            
            db.cur.execute(
                "SELECT user_id, email FROM users WHERE user_id=%s AND mobile=%s",
                (user_id, mobile_no)
            )
            user = db.cur.fetchone()

            if not user:
                print("!Invalid Credential!")
                return False

            
            email = user[1]

            
            otp = OTP_auth.generate_otp()

            
            OTP_auth.send_otp_email(email, otp)
            print("OTP sent to your registered email.")

            
            try:
                user_otp = int(input("Enter OTP: "))
            except ValueError:
                print("Invalid OTP format.")
                return False

            if user_otp == otp:
                current_user_id = user_id
                print("Login successful.")
                return True
            else:
                print("Invalid OTP.")
                return False

            
        except ValueError:
            print("User ID must be numeric")
        except Exception as e:
            print(f"Error Occured: {e}")
            return False
        
    def logout():

        global current_user_id
        current_user_id = None
        print("Logged out successfully.")


    def is_logged_in():
    
        return current_user_id is not None


    def get_logged_user():
    
        return current_user_id