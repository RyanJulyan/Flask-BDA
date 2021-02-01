
# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from flask_login import UserMixin


# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)


# Define a User model
class Email_log(UserMixin, Base):

    __tablename__ = 'email_log'

    # User Name
    user_name = db.Column(db.String(128),  nullable=False)
    # Identification Data: email & password
    sender = db.Column(db.String(128),  nullable=False)
    subject = db.Column(db.String(128),  nullable=False)
    template = db.Column(db.String(128),  nullable=False)
    recipients = db.Column(db.Text,  nullable=False)
    payload = db.Column(db.Text,  nullable=False)

    def __init__(self, user_name, sender, subject, template,
                recipients, payload):
        self.user_name = user_name
        self.sender = sender
        self.subject = subject
        self.template = template
        self.recipients = recipients
        self.payload = payload

    def __repr__(self):
        return '<Email_log %r>' % (self.id)
