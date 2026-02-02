# Banking System

An **Advanced Python & MySQL Banking Project** that simulates core banking operations via a console and script-based interface. This project demonstrates use of Python for backend logic and MySQL for persistent data storage. :contentReference[oaicite:2]{index=2}

---

## 🧠 Overview

This Banking System allows users and admins to perform typical banking tasks including:
- Creating and managing user accounts  
- Deposits and withdrawals  
- Transactions and passbook records  
- Loan processing and authorization  
- Authentication and access control  
- Generating passbook statements

The system uses:
- Python (.py modules) for business logic  
- MySQL for database tables and data persistence  
- Modular code structure for separation of concerns  
- Simple console interface

_All source files like `accounts.py`, `admin.py`, `auth.py`, `db.py`, etc. are included in the repository._ :contentReference[oaicite:3]{index=3}

---

## 📂 Project Structure
Banking-System/
├── .gitignore
├── Authorization.py
├── accounts.py
├── admin.py
├── app.py
├── auth.py
├── db.py
├── loan.py
├── main.py
├── passbook.py
├── transaction.py
└── users.py


Each Python file encapsulates a specific part of the system, such as user management (`users.py`), transactions (`transaction.py`), or database interaction (`db.py`). :contentReference[oaicite:4]{index=4}

---

## 🚀 Features

✔ User registration and login  
✔ Secure authorization for admin operations  
✔ Account creation and details management  
✔ Deposit & withdrawal operations  
✔ Transaction history tracking  
✔ Loan request and processing  
✔ Passbook statement export/print

---

## 🛠 Requirements

Make sure you have the following installed:

- Python 3.x  
- MySQL Server  
- Python packages:  
  ```bash
  pip install mysql-connector-python

💡 Usage Flow

Start application: python main.py

Login or register

Choose from options such as:

Create account

Deposit / Withdraw

Fund transfer

Generate passbook




