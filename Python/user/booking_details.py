from flask import Flask, render_template, request, jsonify
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


def calculate_ticket_price(ticket_type, movie_type):
    base_price = 0

    # Calculate the base price based on the ticket type
    if ticket_type == 'adults':
        base_price += 30
    elif ticket_type == 'children':
        base_price += 20

    # Add additional price for 3D movies
    if movie_type == '3d':
        base_price += 5

    return f"${base_price}"  # Format the base price as a string with the currency symbol

def insert_ticket(movie_code, reservation_status, ticket_price):
    try:
        cursor = db.cursor()
        insert_query = "INSERT INTO ticket (movie_code, reservation_status, ticket_price) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (movie_code, reservation_status, ticket_price))
        db.commit()  # Add this line to commit the changes to the database
        cursor.close()
        return True  # Return True if the insertion is successful
    except Exception as e:
        print("Error inserting ticket:", str(e))
        return False  # Return False if there is an error during insertion
