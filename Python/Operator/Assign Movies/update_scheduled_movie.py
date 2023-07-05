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


def update_scheduled_movie(movie_code, showtime_NO, hall_number):
    cursor = db.cursor()
    try:
        # Delete on movieshowtime table
        update_query_movieshowtime = """
        UPDATE movieshowtime SET showtime_NO = %s, movie_code = %s
        WHERE movie_code = %s AND showtime_NO = %s
        """
        cursor.execute(update_query_movieshowtime, (movie_code, showtime_NO))

        # Delete from hallshowtime table
        update_query_hallshowtime = """
        UPDATE hallshowtime SET showtime_NO = %s, hall_number = %s
        WHERE hall_number = %s AND showtime_NO = %s
        """
        cursor.execute(update_query_hallshowtime, (showtime_NO, hall_number))

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


