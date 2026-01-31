import db

class User:

    def check_user(self,aadhaar):
        check_aadhaar="Select adhaar from users where adhaar=%s"
        values=(aadhaar,)
        db.cur.execute(check_aadhaar,values)
        data=db.cur.fetchone()
        if data:
            return True
        else:
            return False

    def create_user(self):
        try:
            print("Enter Information to create account")
            name=input("Enter your Name: ")
            aadhaar=input("Enter your Adhaar Number: ")
            mobile=input("Enter your Mobile Number: ")

            if not name or not aadhaar or not mobile:
                print("All fields are required. Please try again.")
                return
            
            check_aadhaar=self.check_user(aadhaar)
            if check_aadhaar==True:
                print("User with this Adhaar already exists. Please try again.")
                return

            sql1=("Insert into users(name,aadhaar,mobile) values(%s,%s,%s)")
            values=(name,aadhaar,mobile)
            db.cur.execute(sql1,values)
            db.con.commit()
            print("User registered successfully!")
        except Exception as e:
            print(f"Error Registering User: {e}")
            db.con.rollback()