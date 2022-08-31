
# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
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

    # @aggregated('xyz_count', db.Column(db.Integer))
    # def xyz_count(self):
    #     return db.func.count('1')


# Define a Xyz model
class Xyz(BaseMixin, Base):
    __tablename__ = 'xyz'
    # start new field definitions
    # this line should be removed and replaced with the columns variable
    # end new field definitions
    # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

    # New instance instantiation procedure
    def __init__(self):  # ,example_field):
        # start new instance fields
        # this line should be removed and replaced with the instanceNames variable
        # end new instance fields
        # self.example_field = example_field

    def __repr__(self):
        # Set model quick lookup
        return '<Xyz %r>' % (self.id)
