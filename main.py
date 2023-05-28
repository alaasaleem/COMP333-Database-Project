from flask import Flask, render_template, request, redirect
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


# Define a route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validate the login credentials in your database
        cursor = db.cursor()
        query = "SELECT * FROM user WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            # Redirect to a success page or perform further actions
            return redirect('/success')
        else:
            # Display an error message on the login page
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']  # Add this line

        # Check if the user already exists in the database
        cursor = db.cursor()
        query = "SELECT * FROM user WHERE email = %s"
        cursor.execute(query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = 'User with this email already exists. Please try a different email.'
            return render_template('register.html', error=error)
        else:
            # Insert the new user into the database
            insert_query = "INSERT INTO user (email, password, first_name, last_name) VALUES (%s, %s, %s, %s)"  # Modify the query
            cursor.execute(insert_query, (email, password, first_name, last_name))  # Add first_name and last_name to the values
            db.commit()

            # Redirect to a success page or perform further actions
            return redirect('/success')
    else:
        return render_template('register.html')


# Define a route for the success page
@app.route('/success')
def success():
    return "Login or registration successful!"


if __name__ == '__main__':
    app.run(debug=True)
