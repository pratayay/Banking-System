import db

class User:

    def check_user(self,aadhaar):
        check_aadhaar="Select aadhaar from users where aadhaar=%s"
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
            aadhaar=input("Enter your Aadhaar Number: ")
            if len(str(aadhaar))<12:
                print("!Incoreect Aadhar Number!")
                return
            mobile=input("Enter your Mobile Number: ")
            if len(str(mobile))<10:
                print("!Enter 10 Digit Mobile Number!")
                return
            email=input("Enter Your Mail ID: ")

            if not name or not aadhaar or not mobile:
                print("All fields are required. Please try again.")
                return
            
            check_aadhaar=self.check_user(aadhaar)
            if check_aadhaar==True:
                print("User with this Aadhaar already exists. Please try again.")
                return

            sql1=("Insert into users(name,aadhaar,mobile,Email) values(%s,%s,%s,%s)")
            values=(name,aadhaar,mobile,email)
            db.cur.execute(sql1,values)
            db.con.commit()
            
            print("User registered successfully!")

            userid=db.cur.lastrowid
            print(f"Your User ID is: {userid}")
        except Exception as e:
            print(f"Error Registering User: {e}")
            db.con.rollback()