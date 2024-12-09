from flask_wtf import FlaskForm # Manages rendering specific fields, presents user with a textbox adds validation too
from wtforms import *
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField

class RegisterForm(FlaskForm):
    usernameInput = StringField("Username", validators=[DataRequired()])
    emailInput = StringField("Email", validators=[DataRequired(), Email()])
    passwordInput = PasswordField("Password", validators=[DataRequired(), EqualTo('confirmPasswordInput', message='Passwords must match!')])
    confirmPasswordInput = PasswordField("Confirm Password", validators=[DataRequired()])

class LoginForm(FlaskForm):
    usernameInput = StringField("What's your username", validators=[DataRequired()])
    passwordInput = PasswordField("What's your password", validators=[DataRequired()])

class RecipeForm(FlaskForm):
    nameInput = StringField("Title", validators=[DataRequired()])
    #instructionsInput = StringField("Instructions", validators=[DataRequired()], widget=TextArea())
    instructionsInput = CKEditorField('Instructions', validators=[DataRequired()])

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

class IngredientForm(FlaskForm):
    ingredient = StringField("Ingriedient Name", validators=[DataRequired()])
    def validate_ingredient(self, field):
        field.data = field.data.capitalize()