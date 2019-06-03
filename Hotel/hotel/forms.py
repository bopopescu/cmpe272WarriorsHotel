
# Ref: https://github.com/saltastro/flask-start-setup/blob/master/docs/forms.md
from flask import Flask, render_template, request, flash
from flask_wtf import Form, FlaskForm
# from wtforms import Form
from flask_wtf.csrf import CSRFProtect, CSRFError
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms import DateField, StringField, TextAreaField
from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField, IntegerField


from wtforms_components import TimeField




class DateRangeForm(FlaskForm):
    """A form for entering a date range.

    Default values can be supplied for both the start and date of the range. These will be used if the field value
    isn't set from the GET or POST request parameters.

    CSRF is disabled for this form.

    Params:
    -------
    default_start_date: date
        Default to use as start date.
    default_end_date: date
        Default to use as end date.
    """

    start_date = DateField('Start', validators=[DataRequired()])
    end_date = DateField('End', validators=[DataRequired()])
    submit = SubmitField('Query')

    # def __init__(self, default_start_date=None, default_end_date=None):
    #     Form.__init__(self, csrf_enabled=False)

    #     # change empty fields to default values
    #     if not self.start_date.data and default_start_date:
    #         self.start_date.data = default_start_date
    #     if not self.end_date.data and default_end_date:
    #         self.end_date.data = default_end_date

    # def html(self):
    #     return render_template('calendar.html', form=self)
