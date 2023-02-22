from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app import DATABASE
from flask import flash, session


class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.author = data['author']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.date_created = data['date_created']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls,form):
        data ={
            **form,
            'user_id' : session['uid']
        }
        query = """INSERT INTO recipes (name,author,description,instructions,under_30,date_created,user_id)
                VALUES(%(name)s,%(author)s,%(description)s,%(instructions)s,%(under_30)s,%(date_created)s,%(user_id)s)"""
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for result in results:
            recipes.append(cls(result))
        return recipes

    @classmethod
    def get_one_recipe(cls,id):
        query = "SELECT * FROM recipes WHERE id=%(id)s"
        results = connectToMySQL(DATABASE).query_db(query, {"id":id})
        return cls(results[0])

    @classmethod
    def get_recipe_with_user(cls):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        recipes_w_users = []

        if results:
            for row in results:
                user = User(row)
                recipe_data = {
                    **row,
                    'id' : row['recipes.id'],
                    'created_at' : row['recipes.created_at'],
                    'updated_at' : row['recipes.updated_at']
                }
                recipe = Recipe(recipe_data)
                recipe.user = user
                recipes_w_users.append(recipe)
            return recipes_w_users

    @classmethod
    def update_recipe(cls,data):
        query = """UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s, date_created = %(date_created)s
        WHERE id = %(id)s"""
        results = connectToMySQL(DATABASE).query_db(query,data)
        return results

    @classmethod
    def delete_recipe(cls,id):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query,{"id":id})
        return results

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 2:
            flash("Recipe name is too short!")
            is_valid = False
        
        if len(data['description']) < 1:
            flash("You must enter a description!")
            is_valid = False

        if len(data['instructions']) < 1:
            flash("You must enter instructions!")
            is_valid = False

        if 'under_30' not in data:
            flash("Select Yes or No!")
            is_valid = False

        if data['date_created'] == "":
            flash("Enter a date!")
            is_valid = False

        return is_valid
