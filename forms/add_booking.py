from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms import SelectMultipleField, DateField, StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, NumberRange, InputRequired
import re


class BookingForm(FlaskForm):
    tables = SelectMultipleField('Столики', choices=[i for i in range(1, 7)], coerce=int,
                                 option_widget=widgets.CheckboxInput())
    date = DateField('Дата брони', validators=[InputRequired()])
    start_time = IntegerField(validators=[InputRequired(), NumberRange(0, 23)])
    end_time = IntegerField(validators=[InputRequired(), NumberRange(0, 23)])
    submit = SubmitField('Забронировать')

    def validate_time(form, field):
        if not re.search("^([0-9]|(1[0-9])|(2[0-4]))-([0-9]|(1[0-9])|(2[0-4]))$", field.data):
            raise ValidationError("Invalid input syntax")
    
    def validate_tables(form, field):
        pass
