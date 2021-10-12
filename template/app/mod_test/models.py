
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

    # @aggregated('test_count', db.Column(db.Integer))
    # def test_count(self):
    #     return db.func.count('1')


# Define a Test model
class Test(Base):
    __tablename__ = 'test'
    # start new field definitions
    budget = db.Column(db.Numeric(38, 19), nullable=False, default=False, unique=False, index=True)
    name = db.Column(db.String(50), nullable=False, default=False, unique=True, index=True)
    test_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=False, unique=False, index=True)
    users = db.relationship('Users', remote_side='Users.id', lazy='joined')

    # @aggregated('users_count', db.Column(db.Integer))
    # def users_count(self):
    #     return db.func.count('1')    # this line should be removed and replaced with the columns variable
    # end new field definitions
    # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

    # New instance instantiation procedure
    def __init__(self, budget, name, test_id):  # ,example_field):
        # start new instance fields
        self.budget = budget
        self.name = name
        self.test_id = test_id
        # end new instance fields
        # self.example_field = example_field

    def __repr__(self):
        # Set model quick lookup
        return '<Test %r>' % (self.id)
