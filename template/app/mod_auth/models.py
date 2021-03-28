
# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from flask_login import UserMixin
from app import bcrypt


# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)


# Define a User model
class User(UserMixin, Base):

    __tablename__ = 'users'

    # User Name
    name = db.Column(db.String(128),  nullable=False)
    # Identification Data: email & password
    email = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(192),  nullable=False)
    # Authorisation Data: role & status
    role = db.Column(db.SmallInteger, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)
    # Confirmed account
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    # Authorisation Data: Session
    session_token = db.Column(db.String(100), nullable=True, unique=True)

    def get_id(self):
        return self.session_token

    def __init__(self, name, email, password, role,
                status, confirmed, confirmed_on = None, session_token):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.role = role
        self.status = status
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.session_token = session_token

    def __repr__(self):
        return '<User %r>' % (self.name)
