
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

    # @aggregated('statuses_count', db.Column(db.Integer))
    # def statuses_count(self):
    #     return db.func.count('1')


# Define a Statuses model
class Statuses(Base):
    __tablename__ = 'statuses'
    # start new field definitions
    status_key = db.Column(db.String(256), nullable=False, default=False, unique=True, index=True)
    status_display_name = db.Column(db.String(256), nullable=False, default=False, unique=False, index=False)
    status_description = db.Column(db.Text, nullable=False, default=False, unique=False, index=False)
    status_group = db.Column(db.String(256), nullable=False, default=False, unique=False, index=False)
    key_value = db.Column(db.Text, nullable=True, default=False, unique=False, index=False)    # this line should be removed and replaced with the columns variable
    # end new field definitions
    # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

    # New instance instantiation procedure
    def __init__(self, status_key, status_display_name, status_description, status_group, key_value):  # ,example_field):
        # start new instance fields
        self.status_key = status_key
        self.status_display_name = status_display_name
        self.status_description = status_description
        self.status_group = status_group
        self.key_value = key_value
        # end new instance fields
        # self.example_field = example_field

    def __repr__(self):
        # Set model quick lookup
        return '<Statuses %r>' % (self.id)
