import mysql.connector as sql

con=sql.connect(
    host="localhost",
    user="root",
    password="12345",
    database="banking"
)

cur=con.cursor()