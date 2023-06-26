from flask import Flask, render_template, request, redirect
from login_register import app, validate_login, register_user
from delete_operator import find_operator, delete_operator


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
    if request.method == 'POST':
        search_query = request.form['search_query']
        operator = find_operator(search_query)

        if operator:
            return render_template('delete_operator.html', operators=operator)
        else:
            error = 'Operator not found in the database or operator table.'
            return render_template('delete_operator.html', error=error)

    else:
        return render_template('delete_operator.html')


@app.route('/delete_operator_confirm', methods=['POST'])
def delete_operator_confirm():
    operator_id = request.form['operator_id']
    delete_operator(operator_id)
    return redirect('/manage_operator')

if __name__ == '__main__':
    app.run(debug=True)
