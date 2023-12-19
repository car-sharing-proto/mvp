from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField, 
    SubmitField, 
    BooleanField, 
    TextAreaField, 
    SelectField, 
    DateField,
    TimeField)
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    id = StringField('ID пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Авторизоваться')