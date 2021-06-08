
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

    # @aggregated('api_keys_count', db.Column(db.Integer))
    # def api_keys_count(self):
    #     return db.func.count('1')


# Define a Api_keys model
class Api_keys(Base):
    __tablename__ = 'api_keys'
    # start new field definitions
    api_key = db.Column(db.String(256), nullable=False, default=False, unique=True)
    api_key_notes = db.Column(db.Text, nullable=True, default=False, unique=False)
    created_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=False, unique=False)
    user = db.relationship('User', backref = 'user', remote_side='User.id', lazy='joined')

    @aggregated('user_count', db.Column(db.Integer))
    def user_count(self):
        return db.func.count('1')
    valid_from = db.Column(db.Date, nullable=False, default=False, unique=False)
    valid_to = db.Column(db.Date, nullable=False, default=False, unique=False)
    # end new field definitions
    # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

    # New instance instantiation procedure
    def __init__(self, api_key, api_key_notes, created_user_id, valid_from, valid_to):  # ,example_field):
        # start new instance fields
        self.api_key = api_key
        self.api_key_notes = api_key_notes
        self.created_user_id = created_user_id
        self.valid_from = valid_from
        self.valid_to = valid_to
        # end new instance fields
        # self.example_field = example_field

    def __repr__(self):
        # Set model quick lookup
        return '<Api_keys %r>' % (self.id)
