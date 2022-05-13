from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import re


class RegisterForm(FlaskForm):
    phone = StringField('Телефон', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_phone(form, field):
        text = field.data
        if text.startswith('8'):
            text = text.replace('8', '+7', 1)
        text = text.replace('(', '')
        text = text.replace(')', '')
        text = text.replace('-', '')
        text = text.replace(' ', '')
        if not re.search('^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{5}$', text):
            raise ValidationError("Invalid input syntax")
        form.phone.data = text
