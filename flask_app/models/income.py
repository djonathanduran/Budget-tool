from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from .import user, expense


class Income:
    db_name = "budgeting_tool"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.source_name = db_data['source_name']
        self.amount = db_data['amount']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = []

    @classmethod
    def get_all_incomes(cls):
        query = "SELECT * FROM incomes;"
        incomes_from_db = connectToMySQL(cls.db_name).query_db(query)

        incomes = []
        for income in incomes_from_db:
            incomes.append(cls(income))
        return incomes

    @classmethod
    def add_income(cls, db_data):
        query = "INSERT INTO incomes (source_name, amount, `user_id`) VALUES (%(source_name)s, %(amount)s, %(user_id)s ); "

        return connectToMySQL(cls.db_name).query_db(query, db_data)

    @staticmethod
    def validate_income(data):
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
    def total_income(cls, data):
        query = "SELECT SUM(amount) AS 'total' FROM incomes WHERE incomes.user_id = %(user_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)

        return(results)

    @classmethod
    def update_income(cls, data):
        query = "UPDATE incomes SET source_name = %(source_name)s, amount = %(amount)s WHERE id = %(id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy_income(cls, data):
        query = "DELETE FROM incomes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one_income(cls, data):
        query = "SELECT * FROM incomes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])
