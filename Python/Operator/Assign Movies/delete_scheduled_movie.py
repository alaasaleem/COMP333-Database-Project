from flask import Flask, render_template, request
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

def delete_scheduled_movie_func(movie_code, showtime_NO, hall_number):
    cursor = db.cursor()
    try:
        # Delete from movieshowtime table
        delete_query_movieshowtime = """
        DELETE FROM movieshowtime
        WHERE movie_code = %s AND showtime_NO = %s
        """
        cursor.execute(delete_query_movieshowtime, (movie_code, showtime_NO))

        # Delete from hallshowtime table
        delete_query_hallshowtime = """
        DELETE FROM hallshowtime
        WHERE showtime_NO = %s AND hall_number = %s
        """
        cursor.execute(delete_query_hallshowtime, (showtime_NO, hall_number))

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()




