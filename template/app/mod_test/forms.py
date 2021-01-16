
# Import Form and RecaptchaField (optional)
from flask_wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)


class TestForm(Form):
    # start new form definitions
    name = TextField('name', [Required(message='Must provide a Name')])
    # end new form definitions
    # example_field = TextField('Example Field', [Required(message='Must provide a Example Field')])
