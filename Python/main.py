from flask import Flask, render_template, request, redirect
from login_register import app, validate_login, register_user
from delete_operator import find_operator, delete_operator
from add_operator import add_operator
from list_operators import list_operators
from update_operator import update_operator

app = Flask(__name__)

# Define a route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        role = validate_login(email, password)

        if role == 'user':
            return redirect('/user')
        elif role == 'operator':
            return redirect('/operator')
        elif role == 'admin':
            return redirect('/admin')
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        error = register_user(email, password, first_name, last_name)

        if error:
            return render_template('register.html', error=error)

        # Redirect to a success page or perform further actions
        return redirect('/success')

    else:
        return render_template('register.html')


# Define a route for the operator page
@app.route('/manage_operator')
def manage_operator():
    return render_template('manage_operator.html')

# Define a route for the reports page
@app.route('/manage_reports')
def manage_reports():
    return render_template('manage_reports.html')

@app.route('/delete_operator', methods=['GET', 'POST'])
def delete_operator_route():
    error = None

    if request.method == 'POST':
        search_query = request.form['search_query']
        operator = find_operator(search_query)

        if operator is not None:
            return render_template('delete_operator.html', operators=operator)
        else:
            error = 'Operator not found'

    return render_template('delete_operator.html', error=error)


@app.route('/delete_operator_confirm', methods=['POST'])
def delete_operator_confirm():
    operator_id = request.form['operator_id']
    delete_operator(operator_id)
    return redirect('/manage_operator')


@app.route('/add_operator', methods=['GET', 'POST'])
def add_operator_route():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        error = add_operator(email, password, first_name, last_name)

        if error:
            return render_template('add_operator.html', error=error)
        else:
            success_message = 'Operator added successfully.'
            return render_template('add_operator.html', success_message=success_message)

    else:
        return render_template('add_operator.html')

@app.route('/list_operators')
def list_operators_route():
    operators = list_operators()
    return render_template('list_operators.html', operators=operators)


@app.route('/update_operator', methods=['GET', 'POST'])
def update_operator_route():
    if request.method == 'POST':
        operator_id = request.form['operator_id']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password =  request.form['password']

        existing_operator = find_operator(operator_id)

        if existing_operator is not None:
            update_operator(operator_id, email, first_name, last_name, password)
            success_message = 'Operator updated successfully.'
            return render_template('update_operator.html', success_message=success_message, operator_id=operator_id,
                                   email=email, first_name=first_name, last_name=last_name, password=password)
        else:
            error_message = 'Operator not found.'
            return render_template('update_operator.html', error_message=error_message)

    return render_template('update_operator.html')

if __name__ == '__main__':
    app.run(debug=True)
