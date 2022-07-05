from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField ,TextAreaField 
from wtforms.validators import InputRequired  , Length , Email

class LoginForm(FlaskForm):
    username = StringField('username' , validators=[InputRequired() , Length(min = 5 , max= 20)])
    password = PasswordField('password' , validators=[InputRequired() , Length(min = 8 , max= 30)])

class RegisterForm(FlaskForm):
    email = StringField('email' , validators=[InputRequired() , Email(message = 'Invalid Email') , Length( max= 50)])
    username = StringField('username' , validators=[InputRequired() , Length(min = 5 , max= 20)])
    password = PasswordField('password' , validators=[InputRequired() , Length(min = 8 , max= 30)])

class PostsForm(FlaskForm):
    title = StringField('Title' , validators=[InputRequired() , Length( max= 50)])
    body = TextAreaField('Text' , validators=[InputRequired() , Length( max= 4000)])