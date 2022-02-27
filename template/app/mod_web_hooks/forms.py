
# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)


class Web_hooksForm(Form):
    # start new form definitions
    webhook_name = TextField('webhook_name', [Required(message='Must provide a Webhook name')])
    run_in_module_name = TextField('run_in_module_name', [Required(message='Must provide a Run in module name')])
    run_before_insert = TextField('run_before_insert')
    run_after_insert = TextField('run_after_insert')
    run_before_update = TextField('run_before_update')
    run_after_update = TextField('run_after_update')
    run_before_delete = TextField('run_before_delete')
    run_after_delete = TextField('run_after_delete')
    method = TextField('method', [Required(message='Must provide a Method')])
    data_type = TextField('data_type', [Required(message='Must provide a Data type')])
    api_endpoint = TextField('api_endpoint', [Required(message='Must provide a Api endpoint')])
    api_headers = TextField('api_headers')
    api_params = TextField('api_params')
    active_flag = TextField('active_flag')
    # end new form definitions
    # example_field = TextField('Example Field', [Required(message='Must provide a Example Field')])

    def validate(self):
        initial_validation = super(Web_hooksForm, self).validate()
        
        if not initial_validation:
            return False
        
        return True

