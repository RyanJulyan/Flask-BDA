
# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  
  __abstract__  = True
  id            = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
  created_at    = db.Column(db.DateTime, default=db.func.current_timestamp())
  updated_at    = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
  deleted_at    = db.Column(db.DateTime, nullable=True)

# Define a Xyz model
class Xyz(Base):
  __tablename__ = 'xyz'
  # start new field definitions
  # this line should be removed and replaced with the columns variable
  # end new field definitions

  # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

  # New instance instantiation procedure
  def __init__(self): # ,example_field):
    # start new instance fields
    # this line should be removed and replaced with the instanceNames variable
    # end new instance fields

    #self.example_field = example_field
  
  def __repr__(self):
    return '<Xyz %r>' % (self.name)
