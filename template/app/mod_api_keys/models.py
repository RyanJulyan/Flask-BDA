
# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from dataclasses import dataclass
from app import db

# Import aggregated functionality 
from sqlalchemy_utils import aggregated

from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.properties import ColumnProperty


# Define a base model for other database tables to inherit
class BaseMixin(object):                                                                                                                                                                             
    def as_dict(self):                                                                                                                                                                               
        result = {}                                                                                                                                                                                  
        for prop in class_mapper(self.__class__).iterate_properties:
            if isinstance(prop, ColumnProperty):
                result[prop.key] = getattr(self, prop.key)
        return result


# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), index=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), index=True)
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)

    # @aggregated('api_keys_count', db.Column(db.Integer))
    # def api_keys_count(self):
    #     return db.func.count('1')


# Define a Api_keys model
@dataclass
class Api_keys(BaseMixin, Base):
    __tablename__ = 'api_keys'
    # start new field definitions
    api_key = db.Column(db.String(256), nullable=False, default=False, unique=True, index=True)
    api_key_notes = db.Column(db.Text, nullable=True, default=False, unique=False, index=False)
    created_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=False, unique=False, index=True)
    users = db.relationship('Users', remote_side='Users.id', lazy='joined', innerjoin=True)

    # @aggregated('users_count', db.Column(db.Integer))
    # def users_count(self):
    #     return db.func.count('1')
    valid_from = db.Column(db.DateTime, nullable=False, default=False, unique=False, index=True)
    valid_to = db.Column(db.DateTime, nullable=False, default=False, unique=False, index=True)    # this line should be removed and replaced with the columns variable
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

    @classmethod
    def find_by_api_key(cls, api_key):
        return cls.query.filter_by(api_key=api_key).first()

    def __repr__(self):
        # Set model quick lookup
        return '<Api_keys %r>' % (self.id)
