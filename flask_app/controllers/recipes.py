from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe 


@app.route('/new_recipe')
def new_recipes():
    if not 'uid' in session:
        flash("Access Denied! Login First!")
        return redirect('/')
    
    logged_in_user = User.get_user_by_id(session['uid'])
    # recipes = Recipe.get_recipe_with_user()
    return render_template("new_recipe.html", user = logged_in_user)


@app.route('/create_recipe', methods = ['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/new_recipe')
    Recipe.create(request.form)
    return redirect('/recipes')

@app.route('/update_recipe/<int:id>')
def update_recipe(id):
    if not 'uid' in session:
        flash("Access Denied! Login First!")
        return redirect('/')
    
    logged_in_user = User.get_user_by_id(session['uid'])
    recipe = Recipe.get_one_recipe(id)
    return render_template("update_recipe.html", user = logged_in_user, recipe = recipe)

@app.route('/save_update', methods = ['POST'])
def save_update():
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/update_recipe/{request.form["id"]}')
    Recipe.update_recipe(request.form)
    return redirect('/recipes')

@app.route('/show_recipe/<int:id>')
def show_recipe(id):
    if not 'uid' in session:
        flash("Access Denied! Login First!")
        return redirect('/')
    logged_in_user = User.get_user_by_id(session['uid'])
    recipe = Recipe.get_one_recipe(id)
    return render_template("show_recipe.html",recipe=recipe, user = logged_in_user)

@app.route('/delete_recipe/<int:id>')
def delete_user(id):
    Recipe.delete_recipe(id)
    return redirect('/recipes')
