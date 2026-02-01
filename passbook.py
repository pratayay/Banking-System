import db
import transaction
import os


class Passbook(transaction.Transactions):

    def view_passbook(self):
        try:
            ac_no=int(input("Enter your Account Number: "))
            if not self.is_account_owner(ac_no):
                 print("Entry Denied\nInvalid Account OR Account Not created Yet")
                 return
            C_ac=self.check_account(ac_no)
            if C_ac==False:
                print(f"Account with Account Number:{ac_no} Does not exists. Please try again.")
                return
            
            C2_ac=self.check_ac_status(ac_no)
            if C2_ac==True:
                print(f"Account Number: {ac_no} is inoperable")
                return
            db.cur.execute("Select txn_time, credit, debit, balance from passbook where account_no=%s order by txn_time",(ac_no,))
            rows=db.cur.fetchall()

            if not rows:
                print("No transactions found.")
                return

            # to print Header
            print("\n========== PASSBOOK ==========")
            print(f"Account Number: {ac_no}")
            print("-" * 60)
            print(f"{'Date':<20}{'Credit':<10}{'Debit':<10}{'Balance':<10}")
            print("-" * 60)

            # to print  Rows
            for row in rows:
                date = row[0].strftime("%d-%m-%Y %H:%M")
                credit = row[1]
                debit = row[2]
                balance = row[3]

                print(f"{date:<20}{credit:<10}{debit:<10}{balance:<10}")

            print("-" * 60)

        except Exception as e:
            print("Error viewing passbook:", e)

    def download_passbook(self):
        try:
            ac_no=int(input("Enter your Account Number: "))
            if not self.is_account_owner(ac_no):
                 print("Entry Denied\nInvalid Account OR Account Not created Yet")
                 return
            C_ac=self.check_account(ac_no)
            if C_ac==False:
                print(f"Account with Account Number:{ac_no} Does not exists. Please try again.")
                return
            
            C2_ac=self.check_ac_status(ac_no)
            if C2_ac==True:
                print(f"Account Number: {ac_no} is inoperable")
                return
            db.cur.execute("Select txn_time, credit, debit, balance from passbook where account_no=%s order by txn_time",(ac_no,))
            rows=db.cur.fetchall()

            if not rows:
                print("No transactions found.")
                return
            
            folder = "D:/Personal/Banking-System/Passbook_Statements"
            os.makedirs(folder, exist_ok=True)

            filename = f"{folder}/Statement_{ac_no}.txt"

            mode =  "w"
            with open(filename,mode) as file:
                
                    file.write("=========Passbook=========\n")
                    file.write(f"Account Number: {ac_no}\n")
                    file.write("-"*50+"\n")
                    file.write(f"{'Date':<20}{'Credit':<10}{'Debit':<10}{'Balance':<10}\n")
                
                    file.write("-"*50+"\n")
                    for row in rows:
                        date = row[0].strftime("%d-%m-%Y %H:%M")
                        credit=row[1]
                        debit=row[2]
                        balance=row[3]
                
                        file.write(f"{date:<20}{credit:<10}{debit:<10}{balance:<10}\n")
                    file.write("-"*50)

                    print("Passbook Generated Successfully")

        except Exception as e:
            print("Error Downloading passbook:", e)
