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

def list_operators():
    cursor = db.cursor()

    # Perform a query to fetch all operators
    query = "SELECT * FROM operator"
    cursor.execute(query)
    operators = cursor.fetchall()
    db.commit()
    cursor.close()

    return operators

@app.route('/list_operators')
def operator_list():
    operators = list_operators()
    return render_template('list_operators.html', operators=operators)

if __name__ == '__main__':
    app.run(debug=True)
