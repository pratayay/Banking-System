from users import User
from accounts import Accounts
from transaction import Transactions
from passbook import Passbook
from loan import Loan
import auth


def auth_menu():
    print("\n====== WELCOME ======")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    print("=====================")


def bank_menu():
    print("\n====== BANKING MENU ======")
    print("1. Open Bank Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Transfer Money")
    print("5. View Transaction Log")
    print("6. View Passbook")
    print("7. Download Passbook (TXT)")
    print("8. Loan Services")
    print("9. Logout")
    print("==========================")


def main():
    u = User()
    acc = Accounts()
    txn = Transactions()
    pb = Passbook()
    loan=Loan()
    while True:

        if not auth.Authentication.is_logged_in():
            auth_menu()

            try:
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    auth.Authentication.user_validation()

                elif choice == 2:
                    u.create_user()

                elif choice == 3:
                    print("Thank you for using the Banking System.")
                    break

                else:
                    print("Invalid choice.")

            except ValueError:
                print("Please enter a valid number.")

        
        else:
            bank_menu()

            try:
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    acc.create_account()

                elif choice == 2:
                    txn.deposit()

                elif choice == 3:
                    txn.withdraw()

                elif choice == 4:
                    txn.transfer()

                elif choice == 5:
                    txn.transaction_log()

                elif choice == 6:
                    pb.view_passbook()

                elif choice == 7:
                    pb.download_passbook()

                elif choice==8:
                    loan.menu()

                elif choice == 9:
                    auth.Authentication.logout()

                else:
                    print("Invalid choice.")

            except ValueError:
                print("Please enter a valid number.")


main()
