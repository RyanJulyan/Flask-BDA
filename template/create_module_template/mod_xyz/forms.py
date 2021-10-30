
# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)


class XyzForm(Form):
    # start new form definitions
    # this line should be removed and replaced with the formDefinitions variable
    # end new form definitions
    # example_field = TextField('Example Field', [Required(message='Must provide a Example Field')])

    def validate(self):
        initial_validation = super(XyzForm, self).validate()
        
        if not initial_validation:
            return False
        
        return True

