
# Import Form and RecaptchaField (optional)
from flask_wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)


class Cache_hierarchiesForm(Form):
    # start new form definitions
    organisation_id = TextField('organisation_id', [Required(message='Must provide a Organisation id')]),
    current_hierarchy_id = TextField('current_hierarchy_id', [Required(message='Must provide a Current hierarchy id')]),
    hierarchy_id = TextField('hierarchy_id', [Required(message='Must provide a Hierarchy id')]),
    name = TextField('name', [Required(message='Must provide a Name')]),
    path = TextField('path', [Required(message='Must provide a Path')]),
    level = TextField('level'),
    parent_id = TextField('parent_id'),
    key_value = TextField('key_value')
    # end new form definitions
    # example_field = TextField('Example Field', [Required(message='Must provide a Example Field')])
