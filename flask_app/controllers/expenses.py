from ..models import user, expense
from flask import render_template, redirect, session, request, flash
from flask_app import app


@app.route('/create/expense', methods=['POST'])
def new_expense():
    if not expense.Expense.validate_expense(request.form):
        return redirect("/dashboard")
    data = {
        'source_name': request.form['source_name'],
        'amount': request.form['amount'],
        'user_id': session['user_id']
    }
    expense.Expense.add_expense(data)
    return redirect('/dashboard')


@app.route('/dashboard/expense')
def expense_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    all_expenses = expense.Expense.get_all_expenses()

    return render_template('expense.html', logged_in_user=user.User.get_expense_with_users(data), all_expenses=all_expenses)


@app.route('/edit/<int:user_id>/expense', methods=['get'])
def edit_expense(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': user_id
    }
    user_data = {
        "user_id": session['user_id']
    }
    edit = expense.Expense.get_one_expense(data)
    return render_template('edit_expense.html', edit=edit, this_user=user.User.get_by_id(user_data))


@app.route('/update/expense', methods=["POST"])
def update_expense():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'source_name': request.form['source_name'],
        'amount': request.form['amount'],
        'id': request.form['id']
    }
    expense.Expense.update_expense(data)
    return redirect("/dashboard/expense")


@app.route('/add/expense')
def add_expense():

    data = {
        'user_id': session['user_id']
    }
    return render_template('add_expense.html', logged_in_user=user.User.get_by_id(data))


@app.route('/delete/<int:id>/ex')
def destroy_expense(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    expense.Expense.destroy_expense(data)
    return redirect('/dashboard')
