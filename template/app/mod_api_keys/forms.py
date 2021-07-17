
# Import Form and RecaptchaField (optional)
from flask_wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)


class Api_keysForm(Form):
    # start new form definitions
    api_key = TextField('api_key', [Required(message='Must provide a Api key')]),
    api_key_notes = TextField('api_key_notes'),
    created_user_id = TextField('created_user_id', [Required(message='Must provide a Created user id')]),
    valid_from = TextField('valid_from', [Required(message='Must provide a Valid from')]),
    valid_to = TextField('valid_to', [Required(message='Must provide a Valid to')])
    # end new form definitions
    # example_field = TextField('Example Field', [Required(message='Must provide a Example Field')])
