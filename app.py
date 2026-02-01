import streamlit as st
from datetime import datetime

# -------------------------------------------------
# STREAMLIT CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Banking System", layout="centered")
st.title("🏦 Advanced Banking System (Streamlit)")

# -------------------------------------------------
# SESSION INITIALIZATION
# -------------------------------------------------
if "users" not in st.session_state:
    st.session_state.users = {}  # user_id -> user data

if "accounts" not in st.session_state:
    st.session_state.accounts = {}  # account_no -> account data

if "transactions" not in st.session_state:
    st.session_state.transactions = []  # list of dicts

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "just_registered" not in st.session_state:
    st.session_state.just_registered = False


# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def generate_user_id():
    return len(st.session_state.users) + 1


def generate_account_no():
    return len(st.session_state.accounts) + 1


def user_accounts(user_id):
    return [
        acc_no for acc_no, acc in st.session_state.accounts.items()
        if acc["user_id"] == user_id
    ]


# -------------------------------------------------
# AUTH SCREENS
# -------------------------------------------------
if not st.session_state.logged_in:

    menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

    # ---------------- LOGIN ----------------
    if menu == "Login":
        st.subheader("🔐 Login")

        user_id = st.number_input("User ID", min_value=1, step=1)
        aadhar = st.text_input("Aadhaar Number")
        mobile = st.text_input("Mobile Number")

        if st.button("Login"):
            user = st.session_state.users.get(user_id)
            if user and user["aadhar"] == aadhar and user["mobile"] == mobile:
                st.session_state.logged_in = True
                st.session_state.current_user = user_id
                st.session_state.just_registered = False
                st.success("Login successful")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

    # ---------------- REGISTER ----------------
    else:
        st.subheader("📝 Register")

        name = st.text_input("Name")
        aadhar = st.text_input("Aadhaar")
        mobile = st.text_input("Mobile")

        if st.button("Register"):
            uid = generate_user_id()
            st.session_state.users[uid] = {
                "name": name,
                "aadhar": aadhar,
                "mobile": mobile
            }
            st.session_state.logged_in = True
            st.session_state.current_user = uid
            st.session_state.just_registered = True
            st.success(f"Registered successfully. Your User ID is {uid}")
            st.experimental_rerun()


# -------------------------------------------------
# JUST REGISTERED → OPEN ACCOUNT ONLY
# -------------------------------------------------
elif st.session_state.just_registered:

    st.subheader("🏦 Open Bank Account")

    deposit = st.number_input("Initial Deposit", min_value=0.0)

    if st.button("Create Account"):
        acc_no = generate_account_no()
        st.session_state.accounts[acc_no] = {
            "user_id": st.session_state.current_user,
            "balance": deposit,
            "status": "Active"
        }
        st.success(f"Account created successfully. Account No: {acc_no}")
        st.session_state.just_registered = False
        st.experimental_rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.experimental_rerun()


# -------------------------------------------------
# LOGGED IN – FULL BANKING
# -------------------------------------------------
else:
    st.sidebar.success(f"Logged in as User {st.session_state.current_user}")

    menu = st.sidebar.selectbox(
        "Banking Menu",
        ["Deposit", "Withdraw", "Transfer", "Passbook", "Logout"]
    )

    accounts = user_accounts(st.session_state.current_user)

    if not accounts:
        st.warning("No account found. Please contact support.")
    else:

        # ---------------- DEPOSIT ----------------
        if menu == "Deposit":
            st.subheader("💰 Deposit")
            acc_no = st.selectbox("Account", accounts)
            amount = st.number_input("Amount", min_value=1.0)

            if st.button("Deposit"):
                st.session_state.accounts[acc_no]["balance"] += amount
                st.session_state.transactions.append({
                    "acc": acc_no,
                    "type": "Deposit",
                    "amount": amount,
                    "time": datetime.now()
                })
                st.success("Deposit successful")

        # ---------------- WITHDRAW ----------------
        elif menu == "Withdraw":
            st.subheader("🏧 Withdraw")
            acc_no = st.selectbox("Account", accounts)
            amount = st.number_input("Amount", min_value=1.0)

            if st.button("Withdraw"):
                bal = st.session_state.accounts[acc_no]["balance"]
                if amount > bal:
                    st.error("Insufficient balance")
                else:
                    st.session_state.accounts[acc_no]["balance"] -= amount
                    st.session_state.transactions.append({
                        "acc": acc_no,
                        "type": "Withdraw",
                        "amount": amount,
                        "time": datetime.now()
                    })
                    st.success("Withdrawal successful")

        # ---------------- TRANSFER ----------------
        elif menu == "Transfer":
            st.subheader("🔁 Transfer")
            from_acc = st.selectbox("From Account", accounts)
            to_acc = st.number_input("To Account Number", min_value=1, step=1)
            amount = st.number_input("Amount", min_value=1.0)

            if st.button("Transfer"):
                if to_acc not in st.session_state.accounts:
                    st.error("Target account not found")
                elif amount > st.session_state.accounts[from_acc]["balance"]:
                    st.error("Insufficient balance")
                else:
                    st.session_state.accounts[from_acc]["balance"] -= amount
                    st.session_state.accounts[to_acc]["balance"] += amount
                    st.session_state.transactions.append({
                        "acc": from_acc,
                        "type": "Transfer Out",
                        "amount": amount,
                        "time": datetime.now()
                    })
                    st.session_state.transactions.append({
                        "acc": to_acc,
                        "type": "Transfer In",
                        "amount": amount,
                        "time": datetime.now()
                    })
                    st.success("Transfer successful")

        # ---------------- PASSBOOK ----------------
        elif menu == "Passbook":
            st.subheader("📘 Passbook")
            acc_no = st.selectbox("Account", accounts)

            rows = [
                t for t in st.session_state.transactions
                if t["acc"] == acc_no
            ]

            if rows:
                st.table([
                    {
                        "Date": t["time"].strftime("%d-%m-%Y %H:%M"),
                        "Type": t["type"],
                        "Amount": t["amount"]
                    }
                    for t in rows
                ])
                st.info(f"Current Balance: {st.session_state.accounts[acc_no]['balance']}")
            else:
                st.info("No transactions yet")

        # ---------------- LOGOUT ----------------
        else:
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.success("Logged out")
            st.experimental_rerun()
