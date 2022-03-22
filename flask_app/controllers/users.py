
from ..models import user, income, expense
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if not user.User.validate_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        # 'password': pw_hash
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = user.User.create_user(data)
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route("/login", methods=['POST'])
def login():
    if not user.User.validate_login(request.form):
        return redirect('/')

    data = {
        'email': request.form['email']
    }
    user_with_email = user.User.get_by_email(data)

    if not user_with_email:
        flash("Invalid Email/Password", "error")
        return redirect('/')

    if not bcrypt.check_password_hash(user_with_email.password, request.form['password']):
        return redirect('/')

    session['user_id'] = user_with_email.id
    flash('Congrats, your logged in!', "error")
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    incomes = income.Income.total_income(data)
    expenses = expense.Expense.total_expense(data)

    return render_template('index2.html', logged_in_user=user.User.get_by_id(data), incomes=incomes, expenses=expenses)
