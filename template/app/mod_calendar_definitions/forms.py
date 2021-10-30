
# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)


class Calendar_definitionsForm(Form):
    # start new form definitions
    name = TextField('name', [Required(message='Must provide a Name')]),
    start = TextField('start'),
    end = TextField('end'),
    range_history_periods = TextField('range_history_periods', [Required(message='Must provide a Range history periods')]),
    range_future_periods = TextField('range_future_periods', [Required(message='Must provide a Range future periods')]),
    freq_period_start_day = TextField('freq_period_start_day', [Required(message='Must provide a Freq period start day')]),
    freq_normalize = TextField('freq_normalize', [Required(message='Must provide a Freq normalize')]),
    freq_closed = TextField('freq_closed', [Required(message='Must provide a Freq closed')])
    # end new form definitions
    # example_field = TextField('Example Field', [Required(message='Must provide a Example Field')])

    def validate(self):
        initial_validation = super(Calendar_definitionsForm, self).validate()
        
        if not initial_validation:
            return False
        
        return True

