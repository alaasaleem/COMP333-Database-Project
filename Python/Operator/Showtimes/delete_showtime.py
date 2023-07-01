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

def delete_showtime(showtime_NO):
    cursor = db.cursor()

    # Delete the showtime from the database based on the showtime_number
    delete_query = "DELETE FROM showtime WHERE showtime_NO = %s"
    cursor.execute(delete_query, (showtime_NO,))
    db.commit()
    cursor.close()

    return None
