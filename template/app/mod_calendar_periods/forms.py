
# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)


class Calendar_periodsForm(Form):
    # start new form definitions
    calendar_definition_id = TextField('calendar_definition_id', [Required(message='Must provide a Calendar definition id')]),
    start_date = TextField('start_date', [Required(message='Must provide a Start date')]),
    end_date = TextField('end_date', [Required(message='Must provide a End date')]),
    day = TextField('day', [Required(message='Must provide a Day')]),
    week = TextField('week', [Required(message='Must provide a Week')]),
    week_day = TextField('week_day', [Required(message='Must provide a Week day')]),
    week_index = TextField('week_index', [Required(message='Must provide a Week index')]),
    month = TextField('month', [Required(message='Must provide a Month')]),
    month_index = TextField('month_index', [Required(message='Must provide a Month index')]),
    quarter = TextField('quarter', [Required(message='Must provide a Quarter')]),
    quarter_index = TextField('quarter_index', [Required(message='Must provide a Quarter index')]),
    year = TextField('year', [Required(message='Must provide a Year')])
    # end new form definitions
    # example_field = TextField('Example Field', [Required(message='Must provide a Example Field')])

    def validate(self):
        initial_validation = super(Calendar_periodsForm, self).validate()
        
        if not initial_validation:
            return False
        
        return True

