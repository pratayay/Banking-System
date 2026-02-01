import db
import datetime

class Transactions:

    def check_amount(self,amount):
        if amount<=0:
            return False
        else:
            return True

    def check_account(self,ac_no):
        db.cur.execute("Select 1 from accounts where account_no=%s", (ac_no,))
        data=db.cur.fetchone()
        if data:
            return True
        else:
            return False
        
    def check_ac_status(self,ac_no):
        db.cur.execute("Select status from accounts where account_no=%s And status in ('Blocked','Closed')",(ac_no,))
        data=db.cur.fetchone()
        if data:
            return True
        else:
            return False

    def deposit(self):
        try:
            ac_no=int(input("Enter your Account Number: "))
            C_ac=self.check_account(ac_no)
            if C_ac==False:
                print(f"Account with Account Number:{ac_no} Does not exists. Please try again.")
                return
            
            C2_ac=self.check_ac_status(ac_no)
            if C2_ac==True:
                print(f"Account Number: {ac_no} is inoperable")
                return
            
            amount=float(input("Enter amount to Deposit: "))
            now=datetime.datetime.now()
            
            C_amt=self.check_amount(amount)
            if C_amt==False:
                print("Deposit amount must be greater than zero. Please try again.")
                return
            db.cur.execute("Update accounts set balance=balance+%s where account_no=%s",(amount,ac_no))

            self.update_passbook_credit(ac_no,amount,now)
            
            db.cur.execute("""
                           Insert into transactions(account_no,amount,txn_type,txn_time)
                           values(%s,%s,%s,%s)
                        """,(ac_no,amount,"Deposit",now))
            db.con.commit()
            print("Amount Deposited Successfully!")


        except Exception as e:
            print(f"Error in Deposit: {e}")
            db.con.rollback()

    def update_passbook_credit(self,ac_no,amount,now):
        try:
            db.cur.execute("Select ifnull(balance,0) from accounts where account_no=%s",(ac_no,))
            balance=db.cur.fetchone()[0]
            
            db.cur.execute("Insert into passbook(account_no,credit,debit,balance,txn_time) values(%s,%s,%s,%s,%s)",(ac_no,amount,0,balance,now))

        except Exception as e:
            print(f"Error Occured: {e}")
            db.con.rollback()
    
    def update_passbook_debit(self,ac_no,amount,now):
        try:
            db.cur.execute("Select ifnull(balance,0) from accounts where account_no=%s",(ac_no,))
            balance=db.cur.fetchone()[0]
            
            db.cur.execute("Insert into passbook(account_no,credit,debit,balance,txn_time) values(%s,%s,%s,%s,%s)",(ac_no,0,amount,balance,now))

        except Exception as e:
            print(f"Error Occured: {e}")
            db.con.rollback()

    def withdraw(self):
        try:
            ac_no=int(input("Enter account number: "))
            
            C_ac=self.check_account(ac_no)
            if C_ac==False:
                    print(f"Account with Account Number:{ac_no} Does not exists. Please try again.")
                    return
                
            C2_ac=self.check_ac_status(ac_no)
            if C2_ac==True:
                    print(f"Account Number: {ac_no} is inoperable")
                    return
                
            amount=float(input("Enter amount to Withdraw: "))
            if amount<=0:
                print("!The Withdrwan Amount must be greater than 0!")
                return
            db.cur.execute("Select balance from accounts where account_no=%s",(ac_no,))
            balance=db.cur.fetchone()[0]

            if amount>balance:
                print(f"Insufficient Fund\nCurrent Balance:{balance}")
                return
            now=datetime.datetime.now()
            db.cur.execute("Update accounts set balance=balance-%s where account_no=%s",(amount,ac_no))
            self.update_passbook_debit(ac_no,amount,now)

            db.cur.execute("""
                        Insert into transactions(account_no,txn_type,amount,txn_time)
                        values(%s,%s,%s,%s)
                            """,(ac_no,"Withdraw",amount,now))
            db.con.commit()
            print(f"Amount:{amount} Withdrwan Succesfully!")
        
        except Exception as e:
            print(f"Error Occured: {e}")
            db.con.rollback()

    def transaction_log(self):
        try:
            ac_no=int(input("Enter account number: "))
            
            C_ac=self.check_account(ac_no)
            if C_ac==False:
                    print(f"Account with Account Number:{ac_no} Does not exists. Please try again.")
                    return
                
            C2_ac=self.check_ac_status(ac_no)
            if C2_ac==True:
                    print(f"Account Number: {ac_no} is inoperable")
                    return
            
            db.cur.execute("Select * from transactions where account_no=%s",(ac_no,))
            rows=db.cur.fetchall()

            for row in rows:
                print(row)
        
        except Exception as e:
            print(f"Error Occured: {e}")
            db.con.rollback()

    def transfer(self):
        try:
            ac_no=int(input("Enter account number: "))
            
            C_ac=self.check_account(ac_no)
            if C_ac==False:
                    print(f"Account with Account Number:{ac_no} Does not exists. Please try again.")
                    return
                
            C2_ac=self.check_ac_status(ac_no)
            if C2_ac==True:
                    print(f"Account Number: {ac_no} is inoperable")
                    return
            ac2_no=int(input("Enter Account Number in which You Want To Tranfer: "))
            C_ac2=self.check_account(ac2_no)
            if C_ac2==False:
                    print(f"Account with Account Number:{ac2_no} Does not exists. Please try again.")
                    return
                
            C2_ac2=self.check_ac_status(ac2_no)
            if C2_ac2==True:
                    print(f"Account Number: {ac2_no} is inoperable")
                    return
            
            amount=float("Enter the Amount To Transfer: ")
            
            if amount<=0:
                print("!The Withdrwan Amount must be greater than 0!")
                return
            db.cur.execute("Select balance from accounts where account_no=%s",(ac_no,))
            balance1=db.cur.fetchone()[0]

            if amount>balance1:
                print(f"Insufficient Fund\nCurrent Balance:{balance1}")
                return
            db.cur.execute("select balance from accounts where account_no=%s",(ac2_no,))
            balance2=db.cur.fetchone()[0]
            now=datetime.datetime.now()
            
            db.cur.execute("Update accounts set balance=balance-%s where account_no=%s",(amount,ac_no))
            db.cur.execute("Update accounts set balance=balance+%s where account_no=%s",(amount,ac2_no))

            self.update_passbook_debit(ac_no,amount,now)
            self.update_passbook_credit(ac2_no,amount,now)
            value1=(
                   ac_no,"Transfer",amount,now,
                   ac2_no,"Transfer",amount,now
                   )
            
            db.cur.execute("""
                           Insert into transactions(account_no,txn_type,amount,txn_time)
                           values(%s,%s,%s,%s),
                                 (%s,%s,%s,%s)
                             """,value)
            db.con.commit()
            print("Transfer Successfull!")
        
        except Exception as e:
             print(f"Error Occured: {e}")
             db.con.rollback()