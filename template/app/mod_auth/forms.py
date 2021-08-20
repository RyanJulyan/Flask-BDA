
# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField  # BooleanField

# Import Form validators
from wtforms.validators import Required, DataRequired, Email, Length, EqualTo

# Import module models (i.e. User)
from app.mod_auth.models import User

class LoginForm(Form):
    email = TextField('Email Address', [Email(), Required(message='Email required.')])
    password = PasswordField('Password', [Required(message='Password required.')])


class RegisterForm(Form):
    name = TextField(
        'name',
        validators=[DataRequired(), Length(min=2, max=255)])
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=255)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=8, max=255)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class ForgotForm(Form):
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=255)])

    def validate(self):
        initial_validation = super(ForgotForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append("This email is not registered")
            return False
        return True


class ChangePasswordForm(Form):
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=255)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

