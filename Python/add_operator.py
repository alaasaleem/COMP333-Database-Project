from flask import Flask
import mysql.connector

app = Flask(__name__)

# Configure your MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="DBproject2023!",
    database="bookingsystem"
)

def add_operator(email, password, first_name, last_name):
    cursor = db.cursor()

    # Check if the email already exists in the operator table
    query = "SELECT * FROM operator WHERE email = %s"
    cursor.execute(query, (email,))
    existing_operator = cursor.fetchone()

    if existing_operator:
        return 'Operator with this email already exists. Please try a different email.'

    # Insert the new operator into the operator table
    insert_query = "INSERT INTO operator (email, password, first_name, last_name) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (email, password, first_name, last_name))
    db.commit()

    return None
