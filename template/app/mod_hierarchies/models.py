
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

    # @aggregated('hierarchies_count', db.Column(db.Integer))
    # def hierarchies_count(self):
    #     return db.func.count('1')


# Define a Hierarchies model
class Hierarchies(Base):
    __tablename__ = 'hierarchies'
    # start new field definitions
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'), nullable=False, default=False, unique=False)
    organisations = db.relationship('Organisations', remote_side='Organisations.id', lazy='joined')

    # @aggregated('organisations_count', db.Column(db.Integer))
    # def organisations_count(self):
    #     return db.func.count('1')
    name = db.Column(db.String(256), nullable=False, default=False, unique=False)
    path = db.Column(db.Text, nullable=False, default=False, unique=False)
    level = db.Column(db.Integer, nullable=True, default=False, unique=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('hierarchies.id'), nullable=True, default=False, unique=False)
    hierarchies = db.relationship('Hierarchies', remote_side='Hierarchies.id', lazy='joined')
    cached = db.Column(db.Boolean, nullable=False, default='0', unique=False)

    # @aggregated('hierarchies_count', db.Column(db.Integer))
    # def hierarchies_count(self):
    #     return db.func.count('1')
    key_value = db.Column(db.Text, nullable=True, default=False, unique=False)
    # end new field definitions
    # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

    # New instance instantiation procedure
    def __init__(self, organisation_id, name, path, level, parent_id, key_value, cached):  # ,example_field):
        # start new instance fields
        self.organisation_id = organisation_id
        self.name = name
        self.path = path
        self.level = level
        self.parent_id = parent_id
        self.key_value = key_value
        self.cached = cached
        # end new instance fields
        # self.example_field = example_field

    def __repr__(self):
        # Set model quick lookup
        return '<Hierarchies %r>' % (self.id)

