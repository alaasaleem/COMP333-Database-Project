from flask import Flask, render_template, request, redirect
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

def validate_login(email, password):
    cursor = db.cursor()

    # Check if the user exists in the user table
    query = "SELECT * FROM user WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    if user:
        return 'user'

    # Check if the user exists in the admin table
    query = "SELECT * FROM admin WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    admin = cursor.fetchone()

    if admin:
        return 'admin'

    # Check if the user exists in the operator table
    query = "SELECT * FROM operator WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    operator = cursor.fetchone()

    if operator:
        return 'operator'

    # If the user is not found, return None
    return None

def register_user(email, password, first_name, last_name):
    cursor = db.cursor()

    # Check if the email already exists in the user table
    query = "SELECT * FROM user WHERE email = %s"
    cursor.execute(query, (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return 'User with this email already exists. Please try a different email.'

    # Insert the new user into the user table
    insert_query = "INSERT INTO user (email, password, first_name, last_name) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (email, password, first_name, last_name))
    db.commit()

    return None

# Define a route for the success page
@app.route('/success')
def success():
    # Render the user.html template
    return render_template('user.html')
