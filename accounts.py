import db
from auth import Authentication
class Accounts:

    def check_user(self,user_id):
        db.cur.execute("Select 1 from users where user_id=%s",(user_id,))
        data=db.cur.fetchone()
        if data:
            return True
        else:
            return False
    def check_account(self,user_id):
        check_account="Select 1 from accounts where user_id=%s"
        values=(user_id,)
        db.cur.execute(check_account,values)
        data=db.cur.fetchone()
        if data:
            return True
        else:
            return False

    def create_account(self):
        try:
            

            user_id = Authentication.get_logged_user()
            if user_id is None:
                print("Please Login First")

            
            C1=self.check_account(user_id)
            if C1==True:
                print(f"Account with this User ID:{user_id} already exists. Please try again.")
                return
            while True:
                balance=float(input("Enter amount to Deposit initially: "))
                if balance<0:
                    balance=0
                    print("Initial deposit cannot be negative. Please try again.")
                else:
                    break


            sql1="Insert into accounts(user_id,balance,status) values(%s,%s,%s)"
            values=(user_id,balance,"Active")
            db.cur.execute(sql1,values)
            db.con.commit()

            account_no=db.cur.lastrowid
            print(f"Your Account Number is: {account_no}")
            print("Account created successfully!")
        except Exception as e:
            print(f"Error Opening Account: {e}")
            db.con.rollback()