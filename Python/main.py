import mysql
from flask import Flask, render_template, request, redirect, jsonify
from login_register import validate_login, register_user
from delete_operator import find_operator, delete_operator
from add_operator import add_operator
from list_operators import list_operators
from update_operator import update_operator
from delete_movie import find_movie, delete_movie
from add_movie import add_movie
from list_movies import list_movies
from update_movie import update_movie, find_movie
from add_showtime import add_showtime
from delete_showtime import delete_showtime
from list_showtimes import list_showtimes
from update_showtime import update_showtime, find_showtime_by_NO
from add_scheduled_movie import check_movie_exist, check_showtime_exist, check_record_exist,\
    check_hall_exist, check_showtime_overlap, insert_hall_showtime, insert_movie_showtime, get_showtime_end_time, get_showtime_start_time

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
        password = request.form['password']

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

# Define a route for the operator page
@app.route('/manage_movies')
def manage_movies():
    return render_template('manage_movies.html')

# Define a route for the operator page
@app.route('/schedule_showtimes')
def schedule_showtimes():
    return render_template('schedule_showtimes.html')


@app.route('/delete_movie', methods=['GET', 'POST'])
def delete_movie_route():
    error = None

    if request.method == 'POST':
        search_query = request.form['search_query']
        movie = find_movie(search_query)

        if movie is not None:
            return render_template('delete_movie.html', movies=movie)
        else:
            error = 'Movie not found'

    return render_template('delete_movie.html', error=error)


@app.route('/delete_movie_confirm', methods=['POST'])
def delete_movie_confirm():
    movie_code = request.form['movie_code']
    delete_movie(movie_code)
    return redirect('/manage_movies')


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie_route():
    if request.method == 'POST':
        movie_code = request.form['movie_code']
        title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        run_time = request.form['run_time']

        error = add_movie(movie_code, title, genre, rating, run_time)

        if error:
            return render_template('add_movie.html', error=error)
        else:
            success_message = 'Movie added successfully.'
            return render_template('add_movie.html', success_message=success_message)

    else:
        return render_template('add_movie.html')

@app.route('/list_movies')
def list_movies_route():
    movies = list_movies()
    return render_template('list_movies.html', movies=movies)

@app.route('/update_movie', methods=['GET', 'POST'])
def update_movie_route():
    if request.method == 'POST':
        movie_code = request.form['movie_code']
        title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        run_time = request.form['run_time']

        existing_movie = find_movie(movie_code)

        if existing_movie is not None:
            update_movie(movie_code, title, genre, rating, run_time)
            success_message = 'Movie updated successfully.'
            return render_template('update_movie.html', success_message=success_message, movie_code=movie_code,
                                   title=title, genre=genre, rating=rating, run_time=run_time)
        else:
            error_message = 'Movie not found.'
            return render_template('update_movie.html', error_message=error_message)

    return render_template('update_movie.html')

@app.route('/add_showtime', methods=['GET', 'POST'])
def add_showtime_route():
    if request.method == 'POST':
        showtime_NO = request.form['showtime_NO']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        error = add_showtime(showtime_NO, start_time, end_time)

        if error:
            return render_template('add_showtime.html', error=error)
        else:
            success_message = 'Showtime added successfully.'
            return render_template('add_showtime.html', success_message=success_message)

    else:
        return render_template('add_showtime.html')

@app.route('/delete_showtime', methods=['GET', 'POST'])
def delete_showtime_route():
    error = None

    if request.method == 'POST':
        search_query = request.form['search_query']
        showtime = find_showtime_by_NO(search_query)

        if showtime is not None:
            return render_template('delete_showtime.html', showtimes=showtime)
        else:
            error = 'Showtime not found'

    return render_template('delete_showtime.html', error=error)


@app.route('/delete_showtime_confirm', methods=['POST'])
def delete_showtime_confirm():
    showtime_NO = request.form['showtime_NO']
    delete_showtime(showtime_NO)
    return redirect('/schedule_showtimes')


@app.route('/list_showtimes')
def list_showtimes_route():
    showtimes = list_showtimes()
    return render_template('list_showtimes.html', showtimes=showtimes)

@app.route('/update_showtime', methods=['GET', 'POST'])
def update_showtime_route():
    if request.method == 'POST':
        showtime_NO = request.form['showtime_NO']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        existing_showtime = find_showtime_by_NO(showtime_NO)

        if existing_showtime is not None:
            update_showtime(showtime_NO, start_time, end_time)
            success_message = 'Showtime updated successfully.'
            return render_template('update_showtime.html', success_message=success_message, showtime_NO=showtime_NO,
                                   start_time=start_time, end_time=end_time)
        else:
            error_message = 'Showtime not found.'
            return render_template('update_showtime.html', error_message=error_message)

    return render_template('update_showtime.html')


@app.route('/assign_movie')
def assign_movie():
    return render_template('assign_movie.html')


@app.route('/add_scheduled_movie', methods=['GET', 'POST'])
def add_scheduled_movie():
    if request.method == 'POST':
        movie_code = request.form['movie_code']
        showtime_NO = request.form['showtime_NO']
        hall_number = request.form['hall_number']

        # Retrieve start time and end time based on the showtime number
        start_time = get_showtime_start_time(showtime_NO)
        end_time = get_showtime_end_time(showtime_NO)

        if not check_movie_exist(movie_code):
            error_message = "Movie does not exist."
            return render_template('add_scheduled_movie.html', error_message=error_message)

        if not check_showtime_exist(showtime_NO):
            error_message = "Showtime does not exist."
            return render_template('add_scheduled_movie.html', error_message=error_message)

        if not check_hall_exist(hall_number):
            error_message = "Hall does not exist."
            return render_template('add_scheduled_movie.html', error_message=error_message)

        if check_record_exist(movie_code, showtime_NO, hall_number):
            error_message = "Record already exists."
            return render_template('add_scheduled_movie.html', error_message=error_message)

        if check_showtime_overlap(showtime_NO, hall_number, start_time, end_time):
            error_message = "Showtime overlaps with an existing schedule for the same hall."
            return render_template('add_scheduled_movie.html', error_message=error_message)

        try:
            insert_hall_showtime(showtime_NO, hall_number)
            insert_movie_showtime(movie_code, showtime_NO)

            success_message = "Record added successfully."
            return render_template('add_scheduled_movie.html', success_message=success_message)
        except mysql.connector.errors.IntegrityError:
            error_message = "The showtime for the hall already exists for another movie"
            return render_template('add_scheduled_movie.html', error_message=error_message)

    return render_template('add_scheduled_movie.html')

@app.route('/delete_scheduled_movie')
def delete_scheduled_movie():
    return render_template('delete_scheduled_movie.html')

@app.route('/list_scheduled_movies')
def list_scheduled_movies():
    return render_template('list_scheduled_movies.html')

@app.route('/update_scheduled_movie')
def update_scheduled_movie():
    return render_template('update_scheduled_movie.html')



if __name__ == '__main__':
    app.run(debug=True)
