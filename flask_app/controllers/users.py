from flask import render_template, redirect,request,session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe 
from flask_app import app



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create_user', methods = ['POST'])
def create_user():
    
    if not User.validate(request.form):
        return redirect('/')
        
    User.create_user(request.form)
    return redirect('/')

@app.route('/recipes')
def recipes():
    if not 'uid' in session:
        flash("Access Denied! Login First!")
        return redirect('/')
    
    logged_in_user = User.get_user_by_id(session['uid'])
    recipes = Recipe.get_all_recipes()
    return render_template("recipes.html", user = logged_in_user, recipes = recipes)



@app.route('/secure_login', methods = ['POST'])
def secure_login():
    logged_in_user = User.validate_login(request.form)
    if not logged_in_user:
        return redirect('/')
        
    session['uid'] = logged_in_user.id
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')