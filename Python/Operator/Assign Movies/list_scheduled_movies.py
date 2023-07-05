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

def list_schedule_of_movies():
    cursor = db.cursor()
    query = """
    SELECT movie.movie_code, movie.title, hall.hall_number, showtime.start_time, showtime.end_time
    FROM movie
    JOIN MovieShowtime ON movie.movie_code = MovieShowtime.movie_code
    JOIN showtime ON MovieShowtime.showtime_NO = showtime.showtime_NO
    JOIN HallShowtime ON MovieShowtime.showtime_NO = HallShowtime.showtime_NO
    JOIN hall ON HallShowtime.hall_number = hall.hall_number
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    return result

