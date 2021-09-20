
# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Import aggregated functionality 
from sqlalchemy_utils import aggregated


# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), index=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), index=True)
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)

    # @aggregated('site_settings_count', db.Column(db.Integer))
    # def site_settings_count(self):
    #     return db.func.count('1')


# Define a Site_settings model
class Site_settings(Base):
    __tablename__ = 'site_settings'
    # start new field definitions
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'), nullable=False, default=False, unique=False, index=True)
    organisations = db.relationship('Organisations', remote_side='Organisations.id', lazy='joined')

    # @aggregated('organisations_count', db.Column(db.Integer))
    # def organisations_count(self):
    #     return db.func.count('1')
    key = db.Column(db.String(256), nullable=False, default=False, unique=True, index=True)
    display_name = db.Column(db.String(256), nullable=False, default=False, unique=False, index=False)
    description = db.Column(db.Text, nullable=False, default=False, unique=False, index=False)
    value = db.Column(db.Text, nullable=True, default=False, unique=False, index=False)
    data_type = db.Column(db.String(256), nullable=False, default=False, unique=False, index=False)
    group = db.Column(db.String(256), nullable=False, default=False, unique=False, index=False)
    key_value = db.Column(db.Text, nullable=True, default=False, unique=False, index=False)
    # end new field definitions
    # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

    # New instance instantiation procedure
    def __init__(self, organisation_id, key, display_name, description, value, data_type, group, key_value):  # ,example_field):
        # start new instance fields
        self.organisation_id = organisation_id
        self.key = key
        self.display_name = display_name
        self.description = description
        self.value = value
        self.data_type = data_type
        self.group = group
        self.key_value = key_value
        # end new instance fields
        # self.example_field = example_field

    def __repr__(self):
        # Set model quick lookup
        return '<Site_settings %r>' % (self.id)
