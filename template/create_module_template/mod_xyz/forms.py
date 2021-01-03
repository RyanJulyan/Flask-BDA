
# Import Form and RecaptchaField (optional)
from flask_wtf import Form # , RecaptchaField

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
