from flask import Flask, render_template
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


def list_showtimes():
    cursor = db.cursor()

    # Perform a query to fetch all showtimes
    query = "SELECT * FROM showtime"
    cursor.execute(query)
    showtimes = cursor.fetchall()
    db.commit()
    cursor.close()

    return showtimes

@app.route('/list_showtimes')
def showtime_list():
    showtimes = list_showtimes()
    return render_template('list_showtimes.html', showtimes=showtimes)

if __name__ == '__main__':
    app.run(debug=True)
