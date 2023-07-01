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


def delete_movie(movie_code):
    cursor = db.cursor()

    # Delete the movie from the database based on the movie_code
    delete_query = "DELETE FROM movie WHERE movie_code = %s"
    cursor.execute(delete_query, (movie_code,))
    db.commit()
    cursor.close()

    return None

