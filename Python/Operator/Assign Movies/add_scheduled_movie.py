from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Configure your MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="DBproject2023!",
    database="bookingsystem"
)

def check_movie_exist(movie_code):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM movie WHERE movie_code = %s", (movie_code,))
    movie_exists = cursor.fetchone() is not None
    cursor.close()
    return movie_exists

def check_showtime_exist(showtime_NO):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM showtime WHERE showtime_NO = %s", (showtime_NO,))
    showtime_exists = cursor.fetchone() is not None
    cursor.close()
    return showtime_exists

def check_hall_exist(hall_number):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM hall WHERE hall_number = %s", (hall_number,))
    hall_exists = cursor.fetchone() is not None
    cursor.close()
    return hall_exists

def check_record_exist(movie_code, showtime_NO, hall_number):
    cursor = db.cursor()
    query = """
    SELECT movie.movie_code, movie.title, showtime.start_time, showtime.end_time, hall.hall_number
    FROM movie
    JOIN movieshowtime ON movie.movie_code = movieshowtime.movie_code
    JOIN showtime ON movieshowtime.showtime_NO = showtime.showtime_NO
    JOIN hallshowtime ON movieshowtime.showtime_NO = hallshowtime.showtime_NO
    JOIN hall ON hallshowtime.hall_number = hall.hall_number
    WHERE movie.movie_code = %s AND showtime.showtime_NO = %s AND hall.hall_number = %s
    """
    cursor.execute(query, (movie_code, showtime_NO, hall_number))
    existing_record = cursor.fetchone()
    cursor.close()
    return existing_record is not None


def check_showtime_overlap(showtime_NO, hall_number, start_time, end_time):
    cursor = db.cursor()
    overlap_query = """
    SELECT start_time, end_time
    FROM showtime
    JOIN hallshowtime ON showtime.showtime_NO = hallshowtime.showtime_NO
    WHERE hall_number = %s AND showtime.showtime_NO != %s
    """
    cursor.execute(overlap_query, (hall_number, showtime_NO))
    showtimes = cursor.fetchall()

    start_time_dt = datetime.strptime(start_time[1], "%I:%M %p")
    end_time_dt = datetime.strptime(end_time[1], "%I:%M %p")

    for showtime in showtimes:
        st_dt = datetime.strptime(showtime[0][1], "%I:%M %p")
        et_dt = datetime.strptime(showtime[1][1], "%I:%M %p")

        if (st_dt <= start_time_dt <= et_dt) or (st_dt <= end_time_dt <= et_dt):
            cursor.close()
            return True

    cursor.close()
    return False


def check_showtime_overlap(showtime_NO, hall_number, start_time, end_time):
    cursor = db.cursor()
    overlap_query = """
    SELECT start_time, end_time
    FROM showtime
    JOIN hallshowtime ON showtime.showtime_NO = hallshowtime.showtime_NO
    WHERE hall_number = %s
    """
    cursor.execute(overlap_query, (hall_number,))
    showtimes = cursor.fetchall()

    for showtime in showtimes:
        st_dt = showtime[0]
        et_dt = showtime[1]

        if (st_dt <= start_time <= et_dt) or (st_dt <= end_time <= et_dt):
            cursor.close()
            return True

    cursor.close()
    return False



def insert_hall_showtime(showtime_NO, hall_number):
    cursor = db.cursor()
    try:
        insert_query = """
        INSERT INTO hallshowtime (showtime_NO, hall_number)
        VALUES (%s, %s)
        """
        cursor.execute(insert_query, (showtime_NO, hall_number))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()

def insert_movie_showtime(movie_code, showtime_NO):
    cursor = db.cursor()
    try:
        insert_query = """
        INSERT INTO movieshowtime (movie_code, showtime_NO)
        VALUES (%s, %s)
        """
        cursor.execute(insert_query, (movie_code, showtime_NO))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()

def get_showtime_start_time(showtime_NO):
    cursor = db.cursor()
    query = """
    SELECT start_time
    FROM showtime
    WHERE showtime_NO = %s
    """
    cursor.execute(query, (showtime_NO,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]  # Return the start time string
    return None

def get_showtime_end_time(showtime_NO):
    cursor = db.cursor()
    query = """
    SELECT end_time
    FROM showtime
    WHERE showtime_NO = %s
    """
    cursor.execute(query, (showtime_NO,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]  # Return the end time string
    return None

