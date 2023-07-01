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

def find_operator(operator_id):
    cursor = db.cursor()

    # Perform a search query to fetch operators based on the operator ID
    find_query = "SELECT Operator_ID, first_name, last_name FROM operator WHERE Operator_ID = %s"
    cursor.execute(find_query, (operator_id,))
    existing_operator = cursor.fetchone()

    if not existing_operator:
        return None  # Return None when operator is not found

    cursor.close()

    return existing_operator

def update_operator(operator_id, email, first_name, last_name, password):
    cursor = db.cursor()
    update_query = "UPDATE operator SET email = %s, first_name = %s, last_name = %s, password = %s WHERE Operator_ID = %s"
    cursor.execute(update_query, (email, first_name, last_name, password, operator_id))
    db.commit()

    cursor.close()


