import db
import auth
import datetime

class Loan:

    
    def has_active_loan(self):
        user_id = auth.Authentication.get_logged_user()
        db.cur.execute(
            "SELECT loan_id FROM loans WHERE user_id=%s AND loan_status='Active'",
            (user_id,)
        )
        return db.cur.fetchone()

    
    def menu(self):
        while True:
            print("\n====== LOAN SERVICES ======")
            print("1. Apply for Loan")
            print("2. Pay EMI")
            print("3. View Loan Detail")
            print("4. Back")

            try:
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    if self.has_active_loan():
                        print("You already have an active loan.")
                    else:
                        self.apply_loan()

                elif choice == 2:
                    if not self.has_active_loan():
                        print("No active loan found.")
                    else:
                        self.pay_emi()

                elif choice == 3:
                    if not self.has_active_loan():
                        print("No loan details available.")
                    else:
                        self.view_loan()

                elif choice == 4:
                    break

                else:
                    print("Invalid choice.")

            except ValueError:
                print("Please enter a valid number.")


    def calculate_emi(self, principal, rate, tenure):
        interest = (principal * rate * tenure) / (12 * 100)
        total = principal + interest
        emi = total / tenure
        return round(emi, 2), round(total, 2)


    def apply_loan(self):
        try:
            user_id = auth.Authentication.get_logged_user()

            account_no = int(input("Enter Account Number: "))

            db.cur.execute(
                "SELECT 1 FROM accounts WHERE account_no=%s AND user_id=%s AND status='Active'",
                (account_no, user_id)
            )
            if not db.cur.fetchone():
                print("Invalid or unauthorized account.")
                return

            principal = float(input("Enter Loan Amount: "))
            rate = float(input("Enter Interest Rate (%): "))
            tenure = int(input("Enter Tenure (months): "))

            if principal <= 0 or rate <= 0 or tenure <= 0:
                print("Invalid loan values.")
                return

            emi, total = self.calculate_emi(principal, rate, tenure)
           

            db.cur.execute("""
                INSERT INTO loans
                (user_id, account_no, principal_amount, interest_rate,
                 tenure_months, emi_amount, outstanding_amount,
                 loan_status, applied_on)
                VALUES (%s,%s,%s,%s,%s,%s,%s,'Active',%s)
            """, (
                user_id, account_no, principal, rate,
                tenure, emi, total, datetime.datetime.now()
            ))

            db.cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE account_no=%s",
                (principal, account_no)
            )

            db.con.commit()

            print("\nLoan Applied Successfully!")
            print(f"EMI Amount: {emi}")
            print(f"Total Payable Amount: {total}")

        except Exception as e:
            db.con.rollback()
            print("Error applying loan:", e)

    
    def pay_emi(self):
        try:
            user_id = auth.Authentication.get_logged_user()

            db.cur.execute("""
               SELECT loan_id, account_no, emi_amount, outstanding_amount
               FROM loans
               WHERE user_id=%s
               AND loan_status='Active'
               AND approval_status='Approved'
               """, (user_id,))

            loan = db.cur.fetchone()
            if not loan:
                print("Loan Approval is pending!")
                return

            loan_id     = loan[0]
            acc_no      = loan[1]
            emi         = loan[2]
            outstanding = loan[3]


            db.cur.execute(
                "SELECT balance FROM accounts WHERE account_no=%s",
                (acc_no,)
            )
            balance = db.cur.fetchone()[0]

            if balance < emi:
                print("Insufficient balance.")
                return

            remaining = outstanding - emi
            status = "Closed" if remaining <= 0 else "Active"

            db.cur.execute(
                "UPDATE accounts SET balance = balance - %s WHERE account_no=%s",
                (emi, acc_no)
            )

            db.cur.execute("""
                UPDATE loans
                SET outstanding_amount=%s, loan_status=%s
                WHERE loan_id=%s
            """, (remaining, status, loan_id))

            db.con.commit()

            print("EMI paid successfully.")
            print(f"Remaining Loan Balance: {max(0, remaining)}")

        except Exception as e:
            db.con.rollback()
            print("Error paying EMI:", e)

    
    def view_loan(self):
        user_id = auth.Authentication.get_logged_user()

        db.cur.execute("""
            SELECT loan_id, principal_amount, emi_amount,
                   outstanding_amount, loan_status
            FROM loans
            WHERE user_id=%s
        """, (user_id,))
        loan = db.cur.fetchone()

        print("\n------ LOAN DETAILS ------")
        print(f"Loan ID: {loan[0]}")
        print(f"Principal Amount: {loan[1]}")
        print(f"EMI Amount: {loan[2]}")
        print(f"Outstanding Amount: {loan[3]}")
        print(f"Loan Status: {loan[4]}")
