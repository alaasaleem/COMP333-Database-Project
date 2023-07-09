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

def get_user_bookings(user_email):
    try:
        cursor = db.cursor()
        query = """
        SELECT movie.movie_code, movie.title, hall.hall_number, showtime.start_time, showtime.end_time, ticket.ticket_price
        FROM movie
        JOIN MovieShowtime ON movie.movie_code = MovieShowtime.movie_code
        JOIN showtime ON MovieShowtime.showtime_NO = showtime.showtime_NO
        JOIN HallShowtime ON MovieShowtime.showtime_NO = HallShowtime.showtime_NO
        JOIN hall ON HallShowtime.hall_number = hall.hall_number
        JOIN ticket ON MovieShowtime.movie_code = ticket.movie_code
        JOIN user ON ticket.USER_ID = user.USER_ID
        WHERE user.email = %s
        """

        cursor.execute(query, (user_email,))
        bookings = cursor.fetchall()
        cursor.close()
        return bookings
    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))
        return []
