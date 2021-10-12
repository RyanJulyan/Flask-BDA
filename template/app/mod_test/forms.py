
# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)


class TestForm(Form):
    # start new form definitions
    budget = TextField('budget', [Required(message='Must provide a Budget')])
    name = TextField('name', [Required(message='Must provide a Name')])
    test_id = TextField('test_id', [Required(message='Must provide a Test id')])
    # end new form definitions
    # example_field = TextField('Example Field', [Required(message='Must provide a Example Field')])

    def validate(self):
        initial_validation = super(TestForm, self).validate()
        
        if not initial_validation:
            return False
        
        return True

