
# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)


class StatusesForm(Form):
    # start new form definitions
    status_key = TextField('status_key', [Required(message='Must provide a Status key')])
    status_display_name = TextField('status_display_name', [Required(message='Must provide a Status display name')])
    status_description = TextField('status_description', [Required(message='Must provide a Status description')])
    status_group = TextField('status_group', [Required(message='Must provide a Status group')])
    key_value = TextField('key_value')
    # end new form definitions
    # example_field = TextField('Example Field', [Required(message='Must provide a Example Field')])

    def validate(self):
        initial_validation = super(StatusesForm, self).validate()
        
        if not initial_validation:
            return False
        
        return True

