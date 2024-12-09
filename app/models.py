from app import db
# Password Hashing
from werkzeug.security import generate_password_hash, check_password_hash

#Logging in
from flask_login import UserMixin

class User(db.Model, UserMixin): # User class extends db.Model, required for all models
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)

    password_hash = db.Column(db.String(128), nullable=False)

    # # Override get_id to use UserID instead of id
    # def get_id(self):
    #     return str(self.id)  # Ensure it returns a string

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute!")
    
    # Whatever inside password field and hash it
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Connect User -> Recipe, creates Recipe.user
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return '<Name %r>' % self.username

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)

    # Connect Recipe -> Recipe_Ingredients, creates Recipe_Ingredients.recipe
    recipe_ingredients = db.relationship('Recipe_Ingredients', backref='recipe', lazy='dynamic')

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)

    # Connect Ingredient -> Recipe_Ingredients, creates Recipe_Ingredients.ingredient
    recipe_ingredients = db.relationship('Recipe_Ingredients', backref='ingredient', lazy='dynamic')

    def __str__(self):
        return self.name

class Recipe_Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)