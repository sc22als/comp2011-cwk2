from app import app, db, admin, login_manager, ckeditor
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, login_required, logout_user, current_user
from flask_ckeditor import CKEditor
from sqlalchemy import or_
# Password Hashing
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import *
from . models import *
import datetime
app.app_context().push()

# Flask_Login load user when login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RecipeView(ModelView): # extends ModelView
    can_delete = True
    form_columns = ["user_id", "name", "instructions", "created_at", "updated_at", "recipe_ingredients"]
# Register model with flask admin, add b4 routes:
admin.add_view(ModelView(User, db.session))
admin.add_view(RecipeView(Recipe, db.session))
admin.add_view(ModelView(Ingredient, db.session))
admin.add_view(ModelView(Recipe_Ingredients, db.session))

@app.route('/')
def index():
    title="Homepage"
    return render_template('index.html', title=title)

# # localhost:5000/user/name
# @app.route('/user/<name>')
# def user(name):
#     # Pass the 'name' from the URL to the template
#     return render_template('name.html', title='Hello User', name=name)

#Pass data to NavBar
@app.context_processor
def base(): # Passing data to base.html
    form = SearchForm()
    return dict(form=form)

# Using search bar
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    recipes = Recipe.query
    if form.validate_on_submit():
        searched_term = form.searched.data # Data from search bar
        # Searching through multiple fields in the Recipe model
        recipes = recipes.filter(
            or_(
                User.username.like('%' + searched_term + '%'),
                Recipe.name.like('%' + searched_term + '%'),
                Recipe.instructions.like('%' + searched_term + '%'),
            )
        )
        recipes = recipes.order_by(Recipe.name).all()
        return render_template("search.html", form=form, searched=searched_term, recipes=recipes)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username is already taken
        user = User.query.filter_by(username=form.usernameInput.data).first()
        if user:
            flash("Username already exists.", 'error')
            return redirect('/register')
        
        # Check if email is already taken
        email = User.query.filter_by(email=form.emailInput.data).first()
        if email:
            flash("Email is already registered.", 'error')
            return redirect('/register')
        
        # All checks passed, proceed with registration
        # Hash password
        hashed_pw = generate_password_hash(form.passwordInput.data, "pbkdf2:sha256")
        new_user = User(
            username=form.usernameInput.data,
            email=form.emailInput.data,
            password_hash=hashed_pw,
            created_at=datetime.datetime.now()
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", 'success')
        form.usernameInput.data = ''
        form.emailInput.data = ''
        form.passwordInput.data = ''
        form.confirmPasswordInput.data = ''
        logout_user()
        return redirect(url_for('login'))

    # Handle form validation errors
    if form.emailInput.errors:
        flash("Please enter a valid email address.", 'error')
    if form.passwordInput.errors:
        flash(form.passwordInput.errors[0], 'error')

    return render_template('register.html', title='Register User', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Lookup User by username
        user = User.query.filter_by(username=form.usernameInput.data).first() # returns User() db.model
        if user:
            # Check hash | compare look up user's pw to form pw input
            if check_password_hash(user.password_hash, form.passwordInput.data):
                login_user(user)
                flash("Login Successful!!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("Username not found", 'error')
            return redirect('/login')

    return render_template('login.html', title='Login User', form=form)

# Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You are now logged OUT!")
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    id = current_user.id
    user_to_update = User.query.get_or_404(id)
    form = RegisterForm()
    if request.method == "POST":
        user_to_update.username = request.form['usernameInput']
        user_to_update.email = request.form['emailInput']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return redirect(url_for('dashboard', id=id))
        except:
            flash("Error! User update failed... Try again")
            return render_template("dashboard.html", form=form, user_to_update=user_to_update, id=id)
    else:
        return render_template("dashboard.html", title='Dashboard', form=form, user_to_update=user_to_update, id=id)

# Update User
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    user_to_update = User.query.get_or_404(id)
    form = RegisterForm()
    if request.method == "POST":
        user_to_update.username = request.form['usernameInput']
        user_to_update.email = request.form['emailInput']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return redirect(url_for('dashboard', id=id))
        except:
            flash("Error! User update failed... Try again")
            return render_template("update.html", form=form, user_to_update=user_to_update, id=id)
    else:
        return render_template("update.html", title='Update User', form=form, user_to_update=user_to_update, id=id)

# Delete User
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    form = LoginForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User was deleted!")
        return render_template('login.html', title='Login User', form=form)

    except:
        flash("There was an issue deleting this recipe. Try again..")
        return render_template('login.html', title='Login User', form=form)

@app.route('/get-ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    ingredient_list = [ingredient.name for ingredient in ingredients]
    return jsonify(ingredient_list=ingredient_list)

@app.route('/add-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    # Query all ingredients from the database
    ingredients = Ingredient.query.all()  # This returns list of Ingredient objects

    # Create ingredient
    ingForm = IngredientForm()
    ingredient_name = ingForm.ingredient.data
    print(f"Received ingredient: {ingredient_name}")  # Debug print
    if ingredient_name:
        ingredient_check = Ingredient.query.filter_by(name=ingredient_name).first() 
        if ingredient_check:
            return jsonify({'info': f'{ingredient_name} is already in the database!'})
        try:
            new_ingredient = Ingredient(name=ingredient_name)
            db.session.add(new_ingredient)
            db.session.commit()

            return jsonify({'success': f'{ingredient_name} was added!'})
        except Exception as e:
            return jsonify({'error': f'Error adding ingredient: {str(e)}'}), 400

    # Create Recipe
    form = RecipeForm()
    if form.validate_on_submit():
        print("Form validated successfully")
        new_recipe = Recipe(
            user_id=current_user.id, 
            name=form.nameInput.data, 
            instructions=form.instructionsInput.data, 
            created_at=datetime.datetime.now()
        )
        db.session.add(new_recipe)
        db.session.commit()

        flash("Yum, new recipe added!", 'success')
        # Get the recipe_id immediately after creation
        recipe_id = new_recipe.id
        form.nameInput.data = ''
        form.instructionsInput.data = ''

    # Link Ingredients selected & Recipe created
    selected_ingredients = request.form.get('selected_ingredients', '').split(',')
    for ingredient_name in selected_ingredients:
        ingredient_name = ingredient_name.strip()  # Clean any extra spaces
        if ingredient_name:
            ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
            if ingredient:
                # Create the link between the recipe and ingredient in Recipe_Ingredients table
                recipe_ingredient = Recipe_Ingredients(
                    recipe_id=recipe_id,
                    ingredient_id=ingredient.id,
                )
                db.session.add(recipe_ingredient)
    db.session.commit()

    return render_template("add_recipe.html", title="Add Your Recipe", 
    form=form, ingForm=ingForm, ingredients=ingredients)

@app.route('/recipes')
@login_required
def recipes():
    # Grabbing all recipes
    recipes = Recipe.query.order_by(Recipe.created_at)
    return render_template("recipes.html", title='Recipes', recipes=recipes)

@app.route('/recipes/<int:id>')
@login_required
def recipe(id):
    # Grabbing all recipes
    recipe = Recipe.query.get_or_404(id)
    return render_template("recipe.html", title='Recipe', recipe=recipe)

@app.route('/recipes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeForm()
    if form.validate_on_submit():
        recipe.name = form.nameInput.data
        recipe.instructions = form.instructionsInput.data
        recipe.updated_at = datetime.datetime.now()
        # Update Database
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe Has Been Updated!", "success")
        return redirect(url_for('recipe', id=recipe.id))
    
    if current_user.id == recipe.user.id:
        form.nameInput.data = recipe.name
        form.instructionsInput.data = recipe.instructions
        return render_template("edit_recipe.html", recipe=recipe, form=form)
    else:
        flash("This Recipe Is Not Yours To Edit!")
        return redirect(url_for('recipes', title='Edit Recipe', id=recipe.id))

@app.route('/recipes/delete/<int:id>')
@login_required
def delete_recipe(id):
    recipe_to_delete = Recipe.query.get_or_404(id)
    id = current_user.id
    if id == recipe_to_delete.user.id:
        try:
            db.session.delete(recipe_to_delete)
            db.session.commit()
            flash("Recipe was deleted!")
            # Grabbing all recipes
            recipes = Recipe.query.order_by(Recipe.created_at)
            return render_template("recipes.html", recipes=recipes)

        except:
            flash("There was an issue deleting this recipe. Try again..")
            # Grabbing all recipes
            recipes = Recipe.query.order_by(Recipe.created_at)
            return render_template("recipes.html", recipes=recipes)
    else:
        flash("This Recipe Is Not Yours To Delete!")
        # Grabbing all recipes
        recipes = Recipe.query.order_by(Recipe.created_at)
        return render_template("recipes.html", recipes=recipes)

# Create Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title='404'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(error):
    return render_template("500.html", title='500'), 500