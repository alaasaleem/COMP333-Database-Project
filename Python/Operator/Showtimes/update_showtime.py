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

def find_showtime_by_NO(showtime_NO):
    cursor = db.cursor()

    # Perform a search query to fetch showtimes based on the showtime number
    find_query = "SELECT showtime_NO, start_time, end_time FROM showtime WHERE showtime_NO = %s"
    cursor.execute(find_query, (showtime_NO,))
    existing_showtime = cursor.fetchall()

    if not existing_showtime:
        return None  # Return None when showtime is not found

    db.commit()
    cursor.close()

    return existing_showtime

def update_showtime(showtime_NO, start_time, end_time):
    cursor = db.cursor()
    update_query = "UPDATE showtime SET start_time = %s, end_time = %s  WHERE showtime_NO = %s"
    cursor.execute(update_query, (start_time, end_time, showtime_NO))
    db.commit()

    cursor.close()


