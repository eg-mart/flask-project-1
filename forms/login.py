from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import re


class LoginForm(FlaskForm):
    phone = StringField('Телефон', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

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
        form.phone = text
