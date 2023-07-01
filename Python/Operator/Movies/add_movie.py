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

def add_movie(movie_code, title, genre, rating, run_time):
    cursor = db.cursor()

    # Check if the email already exists in the operator table
    query = "SELECT * FROM movie WHERE movie_code = %s"
    cursor.execute(query, (movie_code,))
    existing_operator = cursor.fetchone()

    if existing_operator:
        return 'Movie with this code already exists.'

    # Insert the new operator into the operator table
    insert_query = "INSERT INTO movie (movie_code, title, genre, rating, run_time) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (movie_code, title, genre, rating, run_time))
    db.commit()

    return None
