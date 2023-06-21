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

        # Check if the user exists in the user table
        query = "SELECT * FROM user WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            role = 'user'
        else:
            # Check if the user exists in the admin table
            query = "SELECT * FROM admin WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            admin = cursor.fetchone()

            if admin:
                role = 'admin'
            else:
                # Check if the user exists in the operator table
                query = "SELECT * FROM operator WHERE email = %s AND password = %s"
                cursor.execute(query, (email, password))
                operator = cursor.fetchone()

                if operator:
                    role = 'operator'
                else:
                    # If the user is not found, show an error
                    error = 'Invalid email or password. Please try again.'
                    return render_template('login.html', error=error)

        # Redirect to the appropriate page based on the role
        if role == 'user':
            return redirect('/user')
        elif role == 'operator':
            return redirect('/operator')
        elif role == 'admin':
            return redirect('/admin')

    else:
        error = None

    # Render the login page
    return render_template('login.html', error=error)

# Define a route for the user page
@app.route('/user')
def user():
    return render_template('user.html')

# Define a route for the operator page
@app.route('/operator')
def operator():
    return render_template('operator.html')

# Define a route for the admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Define a route for the invalid login page
@app.route('/invalid')
def invalid():
    return render_template('invalid.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Check if the email already exists in the user table
        cursor = db.cursor()
        query = "SELECT * FROM user WHERE email = %s"
        cursor.execute(query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = 'User with this email already exists. Please try a different email.'
            return render_template('register.html', error=error)

        # Insert the new user into the user table with the role 'user'
        insert_query = "INSERT INTO user (email, password, first_name, last_name, role) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (email, password, first_name, last_name, 'user'))
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
