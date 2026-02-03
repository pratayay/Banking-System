import db
import datetime


current_admin_id = None
MASTER_ADMIN_KEY = "ADMIN@123"


class Admin:

    def admin_menu(self):
            
        try:
            while True:

                print("\n======Admin Panel======\n")
                print("1. Block Account\n2. Close Account\n3. View Pending Loans\n4. Approve / Reject Loan\n5. Logout")

                
                
                y=int(input("Enter your choice: "))
                if y==1:
                    self.block_account()
                elif y==2:
                    self.close_account
                elif y==3:
                    self.view_pending_loans()
                elif y==4:
                    self.approve_loan()
                elif y==5:
                    print("Logged Out Succesfully")
                    break
                else:
                    print("Invalid Choice!")

        except Exception as e:
            print(f"Error Occured: {e}")
            db.con.rollback()


    def admin_registration(self):
        global MASTER_ADMIN_KEY
        try:
            x=input("Enter Master Key: ")
            if x!=MASTER_ADMIN_KEY:
                print("Unauthorized Access")
                return
            username=input("Enter Username: ")
            password=input("Enter Password: ")

            db.cur.execute("Select username from admins where username=%s",(username,))
            check_username=db.cur.fetchone()

            if check_username:
                print(f"User With Username:{username} Already Exists")
                return

            db.cur.execute("Insert into admins(username,password,created_on) values(%s,%s,%s)",(username,password,datetime.datetime.now()))

            db.con.commit()
            admin_id=db.cur.lastrowid
            print("Admin Account Created Succesfully!")
            print(f"Your admin id is {admin_id}")
        except Exception as e:
            print(f"Error Occured: {e}")
            db.con.rollback()

    def login(self):
        global current_admin_id
        try:
            print("\n====== ADMIN LOGIN ======")
            admin_id = int(input("Enter Admin ID: "))
            password = input("Enter Password: ")

            db.cur.execute(
                "SELECT admin_id FROM admins WHERE admin_id=%s AND password=%s",
                (admin_id, password)
            )
            data = db.cur.fetchone()

            if data:
                current_admin_id = data[0]
                print("Admin login successful.")
            else:
                print("Invalid admin credentials.")

        except ValueError:
            print("Admin ID must be numeric.")
        except Exception as e:
            print("Login error:", e)

    # ---------------- ADMIN LOGOUT ----------------
    def logout(self):
        global current_admin_id
        current_admin_id = None
        print("Admin logged out successfully.")

    def is_logged_in(self):
        return current_admin_id is not None

    def block_account(self):
        try:
            account_no = int(input("Enter Account Number to Block: "))
            reason = input("Reason: ")

            db.cur.execute(
                "SELECT status FROM accounts WHERE account_no=%s",
                (account_no,)
            )
            row = db.cur.fetchone()

            if not row:
                print("Account not found.")
                return

            old_status = row[0]

            if old_status == "Blocked":
                print("Account already blocked.")
                return

            db.cur.execute(
                "UPDATE accounts SET status='Blocked' WHERE account_no=%s",
                (account_no,)
            )

            db.cur.execute("""
                INSERT INTO account_status_logs
                (account_no, old_status, new_status, reason, changed_by, changed_on)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                account_no, old_status, "Blocked", reason,
                current_admin_id, datetime.datetime.now()
            ))

            db.con.commit()
            print("Account blocked successfully.")

        except Exception as e:
            db.con.rollback()
            print("Error blocking account:", e)

    
    def close_account(self):
        try:
            account_no = int(input("Enter Account Number to Close: "))
            reason = input("Reason: ")

            db.cur.execute(
                "SELECT status FROM accounts WHERE account_no=%s",
                (account_no,)
            )
            row = db.cur.fetchone()

            if not row:
                print("Account not found.")
                return

            old_status = row[0]

            if old_status == "Closed":
                print("Account already closed.")
                return

            db.cur.execute(
                "UPDATE accounts SET status='Closed' WHERE account_no=%s",
                (account_no,)
            )

            db.cur.execute("""
                INSERT INTO account_status_logs
                (account_no, old_status, new_status, reason, changed_by, changed_on)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                account_no, old_status, "Closed", reason,
                current_admin_id, datetime.datetime.now()
            ))

            db.con.commit()
            print("Account closed successfully.")

        except Exception as e:
            db.con.rollback()
            print("Error closing account:", e)


    def view_pending_loans(self):
        db.cur.execute("""
            SELECT loan_id, user_id, principal_amount
            FROM loans
            WHERE approval_status='Pending'
        """)
        rows = db.cur.fetchall()

        if not rows:
            print("No pending loans.")
            return

        print("\n--- Pending Loans ---")
        for r in rows:
            print(f"Loan ID: {r[0]} | User ID: {r[1]} | Amount: {r[2]}")

    def approve_loan(self):
        try:
            loan_id = int(input("Enter Loan ID: "))

            db.cur.execute("Select 1 from loans where loan_id=%s and approval_status='Pending'",(loan_id,))
            access=db.cur.fetchone()

            if not access:
                print("No loan found with this ID")
                return
            
            decision = input("Approve or Reject (A/R): ").upper()
            remark = input("Remarks: ")

            if decision not in ("A", "R"):
                print("Invalid choice.")
                return

            status = "Approved" if decision == "A" else "Rejected"

            db.cur.execute("""
                UPDATE loans
                SET approval_status=%s, approved_by=%s, approved_on=%s,
                    loan_status=CASE WHEN %s='Approved' THEN 'Active' ELSE 'Rejected' END
                WHERE loan_id=%s
            """, (
                status, current_admin_id,
                datetime.datetime.now(), status, loan_id
            ))

            db.cur.execute("""
                INSERT INTO loan_approvals
                (loan_id, admin_id, approval_status, remarks, approved_on)
                VALUES (%s,%s,%s,%s,%s)
            """, (
                loan_id, current_admin_id, status,
                remark, datetime.datetime.now()
            ))

            db.con.commit()
            print(f"Loan {status} successfully.")

        except Exception as e:
            db.con.rollback()
            print("Loan approval error:", e)
