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

def add_showtime(showtime_NO, start_time, end_time):
    cursor = db.cursor()

    # Check if the showtime with the same start time and end time already exists in the showtime table
    query = "SELECT * FROM showtime WHERE start_time = %s AND end_time = %s"
    cursor.execute(query, (start_time, end_time))
    existing_showtime = cursor.fetchone()

    if existing_showtime:
        return 'Showtime with the same start time and end time already exists.'

    # Insert the new showtime into the showtime table
    insert_query = "INSERT INTO showtime (showtime_NO, start_time, end_time) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (showtime_NO, start_time, end_time))
    db.commit()

    return None


if __name__ == '__main__':
    app.run()
