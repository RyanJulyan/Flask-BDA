
# Import Form and RecaptchaField (optional)
from flask_wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)


class OrganisationsForm(Form):
    # start new form definitions
    organisation_name = TextField('organisation_name', [Required(message='Must provide a Organisation name')]),
    organisation_details = TextField('organisation_details'),
    organisation_contact_name = TextField('organisation_contact_name', [Required(message='Must provide a Organisation contact name')]),
    organisation_contact_email = TextField('organisation_contact_email', [Required(message='Must provide a Organisation contact email')]),
    organisation_address = TextField('organisation_address'),
    organisation_city = TextField('organisation_city'),
    organisation_postal_code = TextField('organisation_postal_code'),
    organisation_country = TextField('organisation_country'),
    organisation_homepage = TextField('organisation_homepage'),
    organisation_vat_number = TextField('organisation_vat_number'),
    organisation_reg_number = TextField('organisation_reg_number')
    # end new form definitions
    # example_field = TextField('Example Field', [Required(message='Must provide a Example Field')])
