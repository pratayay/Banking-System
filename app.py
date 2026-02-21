from datetime import datetime

import streamlit as st

st.set_page_config(page_title="NovaBank Digital", page_icon="🏦", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #14213d 0%, #0b132b 45%, #020617 100%);
        color: #f8fafc;
    }
    .hero {
        padding: 1.4rem 1.8rem;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(16,185,129,0.18), rgba(99,102,241,0.22));
        border: 1px solid rgba(148,163,184,0.25);
        box-shadow: 0 10px 35px rgba(2, 6, 23, 0.45);
        margin-bottom: 1rem;
    }
    .hero h1 { margin: 0; font-size: 2rem; }
    .hero p { margin: 0.3rem 0 0; color: #cbd5e1; }
    .metric-card {
        border-radius: 14px;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.25);
        padding: 0.9rem;
        text-align: center;
    }
    .metric-label { color: #94a3b8; font-size: 0.82rem; text-transform: uppercase; letter-spacing: .06em; }
    .metric-value { color: #f8fafc; font-size: 1.3rem; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

for key, value in {
    "users": {},
    "accounts": {},
    "transactions": [],
    "logged_in": False,
    "current_user": None,
    "just_registered": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = value


def generate_user_id():
    return len(st.session_state.users) + 1


def generate_account_no():
    return len(st.session_state.accounts) + 100001


def user_accounts(user_id):
    return [
        acc_no
        for acc_no, acc in st.session_state.accounts.items()
        if acc["user_id"] == user_id
    ]


def add_transaction(acc_no, t_type, amount):
    st.session_state.transactions.append(
        {
            "acc": acc_no,
            "type": t_type,
            "amount": round(amount, 2),
            "time": datetime.now(),
        }
    )


def render_hero(user_id=None):
    welcome = "Your AI-powered personal banking workspace"
    if user_id:
        welcome = f"Welcome back, {st.session_state.users[user_id]['name']}"
    st.markdown(
        f"""
        <div class="hero">
            <h1>🏦 NovaBank Digital Experience</h1>
            <p>{welcome}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics(accounts):
    total_balance = sum(st.session_state.accounts[a]["balance"] for a in accounts)
    total_txns = len([t for t in st.session_state.transactions if t["acc"] in accounts])
    cols = st.columns(3)
    data = [
        ("Accounts", str(len(accounts))),
        ("Portfolio Value", f"₹{total_balance:,.2f}"),
        ("Transactions", str(total_txns)),
    ]
    for col, (label, val) in zip(cols, data):
        col.markdown(
            f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{val}</div></div>",
            unsafe_allow_html=True,
        )


def render_login_register():
    render_hero()
    left, right = st.columns([1, 1])

    with left:
        st.subheader("🔐 Sign In")
        with st.form("login_form"):
            user_id = st.number_input("User ID", min_value=1, step=1)
            aadhar = st.text_input("Aadhaar Number")
            mobile = st.text_input("Mobile Number")
            login_btn = st.form_submit_button("Login")

        if login_btn:
            user = st.session_state.users.get(user_id)
            if user and user["aadhar"] == aadhar and user["mobile"] == mobile:
                st.session_state.logged_in = True
                st.session_state.current_user = user_id
                st.session_state.just_registered = False
                st.success("Login successful")
                st.rerun()
            st.error("Invalid credentials")

    with right:
        st.subheader("✨ Create Profile")
        with st.form("register_form"):
            name = st.text_input("Full Name")
            aadhar = st.text_input("Aadhaar")
            mobile = st.text_input("Mobile")
            register_btn = st.form_submit_button("Register")

        if register_btn:
            if not (name and aadhar and mobile):
                st.warning("All fields are required.")
                return
            uid = generate_user_id()
            st.session_state.users[uid] = {"name": name, "aadhar": aadhar, "mobile": mobile}
            st.session_state.logged_in = True
            st.session_state.current_user = uid
            st.session_state.just_registered = True
            st.success(f"Profile created. Your User ID is {uid}")
            st.rerun()


def render_open_account():
    render_hero(st.session_state.current_user)
    st.subheader("Open your first premium account")
    with st.form("open_account"):
        deposit = st.number_input("Initial Deposit", min_value=0.0, step=100.0)
        create = st.form_submit_button("Create Account")

    if create:
        acc_no = generate_account_no()
        st.session_state.accounts[acc_no] = {
            "user_id": st.session_state.current_user,
            "balance": round(deposit, 2),
            "status": "Active",
        }
        if deposit > 0:
            add_transaction(acc_no, "Initial Deposit", deposit)
        st.session_state.just_registered = False
        st.success(f"Account {acc_no} is now active.")
        st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()


def render_dashboard():
    uid = st.session_state.current_user
    accounts = user_accounts(uid)

    render_hero(uid)
    st.sidebar.success(f"Logged in as User {uid}")

    if not accounts:
        st.warning("No account found. Please create an account.")
        if st.button("Create My First Account"):
            st.session_state.just_registered = True
            st.rerun()
        return

    render_metrics(accounts)
    st.markdown("### Banking Workspace")
    tabs = st.tabs(["💰 Deposit", "🏧 Withdraw", "🔁 Transfer", "📘 Passbook"])

    with tabs[0]:
        acc_no = st.selectbox("Account", accounts, key="dep_acc")
        amount = st.number_input("Deposit Amount", min_value=1.0, key="dep_amt")
        if st.button("Add Funds"):
            st.session_state.accounts[acc_no]["balance"] += amount
            add_transaction(acc_no, "Deposit", amount)
            st.success("Deposit successful")
            st.rerun()

    with tabs[1]:
        acc_no = st.selectbox("Account", accounts, key="with_acc")
        amount = st.number_input("Withdraw Amount", min_value=1.0, key="with_amt")
        if st.button("Withdraw Cash"):
            bal = st.session_state.accounts[acc_no]["balance"]
            if amount > bal:
                st.error("Insufficient balance")
            else:
                st.session_state.accounts[acc_no]["balance"] -= amount
                add_transaction(acc_no, "Withdraw", amount)
                st.success("Withdrawal successful")
                st.rerun()

    with tabs[2]:
        from_acc = st.selectbox("From Account", accounts, key="tr_from")
        to_acc = st.number_input("To Account Number", min_value=100001, step=1)
        amount = st.number_input("Transfer Amount", min_value=1.0, key="tr_amt")
        if st.button("Send Money"):
            if to_acc not in st.session_state.accounts:
                st.error("Target account not found")
            elif amount > st.session_state.accounts[from_acc]["balance"]:
                st.error("Insufficient balance")
            else:
                st.session_state.accounts[from_acc]["balance"] -= amount
                st.session_state.accounts[to_acc]["balance"] += amount
                add_transaction(from_acc, "Transfer Out", amount)
                add_transaction(to_acc, "Transfer In", amount)
                st.success("Transfer successful")
                st.rerun()

    with tabs[3]:
        acc_no = st.selectbox("Account", accounts, key="pb_acc")
        rows = [t for t in st.session_state.transactions if t["acc"] == acc_no]
        st.info(f"Current Balance: ₹{st.session_state.accounts[acc_no]['balance']:,.2f}")
        if rows:
            st.dataframe(
                [
                    {
                        "Date": t["time"].strftime("%d-%m-%Y %H:%M"),
                        "Type": t["type"],
                        "Amount": f"₹{t['amount']:,.2f}",
                    }
                    for t in sorted(rows, key=lambda x: x["time"], reverse=True)
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.caption("No transactions yet.")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()


if not st.session_state.logged_in:
    render_login_register()
elif st.session_state.just_registered:
    render_open_account()
else:
    render_dashboard()
