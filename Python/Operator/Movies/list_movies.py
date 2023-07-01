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

def list_movies():
    cursor = db.cursor()

    # Perform a query to fetch all movies
    query = "SELECT * FROM movie"
    cursor.execute(query)
    movies = cursor.fetchall()
    db.commit()
    cursor.close()

    return movies

@app.route('/list_movies')
def movie_list():
    movies = list_movies()
    return render_template('list_movies.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
