from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ItemListingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    condition = StringField('Condition', validators=[DataRequired()])
    submit = SubmitField('Create Listing')