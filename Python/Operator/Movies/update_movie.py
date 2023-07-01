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

def find_movie(movie_code):
    cursor = db.cursor()

    # Perform a search query to fetch movies based on the movie code
    find_query = "SELECT movie_code, title, genre, rating, run_time FROM movie WHERE movie_code = %s"
    cursor.execute(find_query, (movie_code,))
    existing_movie = cursor.fetchall()

    if not existing_movie:
        return None  # Return None when movie is not found

    db.commit()
    cursor.close()

    return existing_movie

def update_movie(movie_code, title, genre, rating, run_time):
    cursor = db.cursor()
    update_query = "UPDATE movie SET title = %s, genre = %s, rating = %s, run_time = %s  WHERE movie_code = %s"
    cursor.execute(update_query, (title, genre, rating, run_time, movie_code))
    db.commit()

    cursor.close()


