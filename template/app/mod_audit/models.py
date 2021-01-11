
# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)


# Define a User model
class Audit(Base):

    __tablename__ = 'model_audit'

    # User Name
    model_name = db.Column(db.String(256),  nullable=False)
    action = db.Column(db.String(256),  nullable=False)
    context = db.Column(db.Text,  nullable=False)
    payload = db.Column(db.Text,  nullable=False)

    def __init__(self, model_name, action, context, payload):
        self.model_name = model_name
        self.action = action
        self.context = context
        self.payload = payload

    def __repr__(self):
        return '<Audit %r>' % (self.model_name)
