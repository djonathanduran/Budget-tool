from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from .import user, income


class Expense:
    db_name2 = "budgeting_tool"

    def __init__(self, db_data2):
        self.id = db_data2['id']
        self.source_name = db_data2['source_name']
        self.amount = db_data2['amount']
        self.created_at = db_data2['created_at']
        self.updated_at = db_data2['updated_at']
        self.user = []

    @classmethod
    def get_all_expenses(cls):
        query = "SELECT * FROM expenses;"
        expenses_from_db = connectToMySQL(cls.db_name2).query_db(query)

        expenses = []
        for expense in expenses_from_db:
            expenses.append(cls(expense))
        return expenses

    @classmethod
    def add_expense(cls, db_data2):
        query = "INSERT INTO expenses (source_name, amount, `user_id`) VALUES (%(source_name)s, %(amount)s, %(user_id)s ); "

        return connectToMySQL(cls.db_name2).query_db(query, db_data2)

    @staticmethod
    def validate_expense(data):
        is_valid = True
        if len(data['source_name']) < 2:
            is_valid = False
            flash("Source Name must be more than 2 charcters", "error2")
        if len(data['amount']) < 0:
            is_valid = False
            flash("Amount must be more than $0", "error2")
        if len(data['amount']) == 0:
            is_valid = False
            flash("Amount is required", "error2")
        return is_valid

    @classmethod
    def total_expense(cls, data):
        query = "SELECT SUM(amount) AS 'total' FROM expenses WHERE expenses.user_id = %(user_id)s"
        results = connectToMySQL(cls.db_name2).query_db(query, data)
        print(results)
        return results

    @classmethod
    def update_expense(cls, data):
        query = "UPDATE expenses SET source_name = %(source_name)s, amount = %(amount)s WHERE id = %(id)s"
        return connectToMySQL(cls.db_name2).query_db(query, data)

    @classmethod
    def destroy_expense(cls, data):
        query = "DELETE FROM expenses WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name2).query_db(query, data)

    @classmethod
    def get_one_expense(cls, data):
        query = "SELECT * FROM expenses WHERE id = %(user_id)s;"
        results = connectToMySQL(cls.db_name2).query_db(query, data)
        return cls(results[0])
