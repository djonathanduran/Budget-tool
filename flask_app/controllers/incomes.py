from ..models import user, income
from flask import render_template, redirect, session, request, flash
from flask_app import app


@app.route('/create/income', methods=['POST'])
def new_income():
    if not income.Income.validate_income(request.form):
        return redirect("/dashboard")
    data = {
        'source_name': request.form['source_name'],
        'amount': request.form['amount'],
        'user_id': session['user_id']
    }
    income.Income.add_income(data)
    return redirect('/dashboard')


@app.route('/dashboard/income')
def income_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    all_incomes = income.Income.get_all_incomes()

    return render_template('income.html', logged_in_user=user.User.get_income_with_users(data), all_incomes=all_incomes)


@app.route('/edit/<int:user_id>', methods=['get'])
def edit_income(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': user_id
    }
    user_data = {
        "user_id": session['user_id']
    }
    edit = income.Income.get_one_income(data)
    return render_template('edit_income.html', edit=edit, this_user=user.User.get_by_id(user_data))


@app.route('/update/income', methods=["POST"])
def update_income():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'source_name': request.form['source_name'],
        'amount': request.form['amount'],
        'id': request.form['id']
    }
    income.Income.update_income(data)
    return redirect("/dashboard/income")


@app.route('/add/income')
def add_income():

    data = {
        'user_id': session['user_id']
    }
    return render_template('add_income.html', logged_in_user=user.User.get_by_id(data))


@app.route('/delete/<int:id>')
def destroy_income(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    income.Income.destroy_income(data)
    return redirect('/dashboard')
