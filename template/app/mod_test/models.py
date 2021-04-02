
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

    # @aggregated('test_count', db.Column(db.Integer))
    # def test_count(self):
    #     return db.func.count('1')


# Define a Test model
class Test(Base):
    __tablename__ = 'test'
    # start new field definitions
    name = db.Column(db.String(256), nullable=False, default=False, unique=True)
    # end new field definitions
    # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

    # New instance instantiation procedure
    def __init__(self, name):  # ,example_field):
        # start new instance fields
        self.name = name
        # end new instance fields
        # self.example_field = example_field

    def __repr__(self):
        # Set model quick lookup
        return '<Test %r>' % (self.id)
