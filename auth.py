import db
import users

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
            user_id=int(input("Enter User ID: "))
            
            aadhar=input("Enter Aadhar Number: ")
            mobile_no=input("Enter Mobile Number: ")

            db.cur.execute("Select user_id from users where user_id=%s And aadhaar=%s and mobile=%s",(user_id,aadhar,mobile_no))
            valid=db.cur.fetchone()

            if valid:
                current_user_id=valid[0]
                return True
            else:
               print("!Invalid Credential!")
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