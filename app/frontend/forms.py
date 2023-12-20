from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
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

class RentForm(FlaskForm):
    cars = SelectField('Автомобиль', validators=[DataRequired()],render_kw={"class": "custom-select"})
    submit = SubmitField('Забронировать')

class AddUserForm(FlaskForm):
    id = StringField('ID пользователя', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    role = SelectField('Роль', validators=[DataRequired()],render_kw={"class": "custom-select"})

class EditUserForm(FlaskForm):
    password = StringField('Пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    role = SelectField('Роль', validators=[DataRequired()],render_kw={"class": "custom-select"})

class AddCarForm(FlaskForm):
    id = StringField('ID автомобиля', validators=[DataRequired()])
    mark_id = SelectField('Модель', validators=[DataRequired()],render_kw={"class": "custom-select"})
    number = StringField('Гос. номер', validators=[DataRequired()])