
# Import flask render template for email teplate 
from flask import render_template

# Import mail message to compile a message
from flask_mail import Message

# Import the database object from the main app module
from app import app, mail

def send_email(to, subject, template, data):

    html = render_template(template, data=data)

    msg = Message(
        subject,
        recipients=[to],
        html=html,
        sender=(app.config['MAIL_FROM_NAME'], app.config['MAIL_FROM_ADDRESS'])
    )

    mail.send(msg)