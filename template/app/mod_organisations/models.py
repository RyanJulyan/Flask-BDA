
# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Import aggregated functionality 
from sqlalchemy_utils import aggregated


# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

    # @aggregated('organisations_count', db.Column(db.Integer))
    # def organisations_count(self):
    #     return db.func.count('1')


# Define a Organisations model
class Organisations(Base):
    __tablename__ = 'organisations'
    # start new field definitions
    organisation_name = db.Column(db.String(256), nullable=False, default=False, unique=True)
    organisation_logo = db.Column(db.Text, nullable=True, default=False, unique=False)
    organisation_description = db.Column(db.Text, nullable=True, default=False, unique=True)
    organisation_industry = db.Column(db.String(256), nullable=True, default=False, unique=False)
    organisation_contact_name = db.Column(db.String(256), nullable=False, default=False, unique=False)
    organisation_contact_email = db.Column(db.String(256), nullable=False, default=False, unique=True)
    organisation_binding_database_uri = db.Column(db.Text, nullable=False, default=False, unique=True)
    organisation_address = db.Column(db.Text, nullable=True, default=False, unique=False)
    organisation_city = db.Column(db.String(256), nullable=True, default=False, unique=False)
    organisation_postal_code = db.Column(db.String(256), nullable=True, default=False, unique=False)
    organisation_country = db.Column(db.String(256), nullable=True, default=False, unique=False)
    organisation_homepage = db.Column(db.Text, nullable=True, default=False, unique=False)
    organisation_vat_number = db.Column(db.Text, nullable=True, default=False, unique=False)
    organisation_reg_number = db.Column(db.Text, nullable=True, default=False, unique=False)
    # end new field definitions
    # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

    # New instance instantiation procedure
    def __init__(self, organisation_name, organisation_logo, organisation_description, organisation_industry, organisation_contact_name, organisation_contact_email, organisation_binding_database_uri, organisation_address, organisation_city, organisation_postal_code, organisation_country, organisation_homepage, organisation_vat_number, organisation_reg_number):  # ,example_field):
        # start new instance fields
        self.organisation_name = organisation_name
        self.organisation_logo = organisation_logo
        self.organisation_description = organisation_description
        self.organisation_industry = organisation_industry
        self.organisation_contact_name = organisation_contact_name
        self.organisation_contact_email = organisation_contact_email
        self.organisation_binding_database_uri = organisation_binding_database_uri
        self.organisation_address = organisation_address
        self.organisation_city = organisation_city
        self.organisation_postal_code = organisation_postal_code
        self.organisation_country = organisation_country
        self.organisation_homepage = organisation_homepage
        self.organisation_vat_number = organisation_vat_number
        self.organisation_reg_number = organisation_reg_number
        # end new instance fields
        # self.example_field = example_field

    def __repr__(self):
        # Set model quick lookup
        return '<Organisations %r>' % (self.id)
