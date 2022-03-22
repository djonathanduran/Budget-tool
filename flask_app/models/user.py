
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from .import income, expense


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = "budgeting_tool"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.incomes = []
        self.expenses = []

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, `password`) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s );"

        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_registration(data):
        is_valid = (True)
        # special_characters = [':', "#", "!"]
        # if special_characters not in data['password']
        if len(data["first_name"]) == 0:
            is_valid = False
            flash("First name is required", "error")
        if len(data["last_name"]) == 0:
            is_valid = False
            flash("Last name is required", "error")
        if len(data['password']) < 8:
            is_valid = False
            flash("password must be at least 8 characters long", "error")
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "error")
            is_valid = False
        if data['password'] != data['confirm_password']:
            is_valid = False
            flash("Passwords don't match", "error")
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, data)
        # print(f"results: {results}")
        # print(f"length of results: {len(results)}")
        # if len(results) >= 1:
        #     is_valid = False
        #     flash("Email is already taken", "error")
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) == 0:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) == 0:
            return False
        return cls(results[0])

    @staticmethod
    def validate_login(data):
        is_valid = (True)
        if len(data['email']) == 0:
            is_valid = False
            flash("An Email is required", "error")
        if len(data['password']) == 0:
            is_valid = False
            flash("An Password is required", "error")
        return is_valid

    @classmethod
    def get_income_with_users(cls, data):
        query = "SELECT * FROM users LEFT JOIN incomes ON `user_id` = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        this_user = cls(results[0])
        for row_from_db in results:

            income_data = {
                "id": row_from_db["incomes.id"],
                "source_name": row_from_db["source_name"],
                "amount": row_from_db['amount'],
                "user_id": row_from_db["user_id"],
                "created_at": row_from_db["incomes.created_at"],
                "updated_at": row_from_db["incomes.updated_at"]
            }
            if income_data['id']:
                this_user.incomes.append(income.Income(income_data))
        return this_user

    @classmethod
    def get_expense_with_users(cls, data):
        query = "SELECT * FROM users LEFT JOIN expenses ON `user_id` = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        this_user = cls(results[0])
        for row_from_db in results:

            expense_data = {
                "id": row_from_db["expenses.id"],
                "source_name": row_from_db["source_name"],
                "amount": row_from_db['amount'],
                "user_id": row_from_db["user_id"],
                "created_at": row_from_db["expenses.created_at"],
                "updated_at": row_from_db["expenses.updated_at"]
            }
            if expense_data['id']:
                this_user.expenses.append(expense.Expense(expense_data))
        return this_user
