
# Import Form and RecaptchaField (optional)
from flask_wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)


class Site_settingsForm(Form):
    # start new form definitions
    organisation_id = TextField('organisation_id', [Required(message='Must provide a Organisation id')]),
    key = TextField('key', [Required(message='Must provide a Key')]),
    display_name = TextField('display_name', [Required(message='Must provide a Display name')]),
    description = TextField('description', [Required(message='Must provide a Description')]),
    value = TextField('value'),
    data_type = TextField('data_type', [Required(message='Must provide a Data type')]),
    group = TextField('group', [Required(message='Must provide a Group')]),
    key_value = TextField('key_value')
    # end new form definitions
    # example_field = TextField('Example Field', [Required(message='Must provide a Example Field')])
