
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import flask login 
from flask_login import login_user, logout_user, login_required, current_user

# URL safe serializers
from itsdangerous import URLSafeTimedSerializer

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import date time
import datetime

# Import mobile template
from flask_mobility.decorators import mobile_template

# Import the database object from the main app module
from app import db, app

# Import module forms
from app.mod_auth.forms import LoginForm, RegisterForm, ChangePasswordForm, ForgotForm

# Import module models (i.e. User)
from app.mod_auth.models import User

# Import send_email
from app.mod_email.controllers import send_email

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, template_folder='templates', url_prefix = '/auth')


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('user.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration = 10800):  # expiration = 10800 = 3 hours
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


# Set the route and accepted methods
@mod_auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            name = form.email.data,
            email = form.email.data,
            password = form.password.data,
            role = 1,
            status = 1,
            confirmed = False,
            confirmed_on = None,
            session_token = None
        )
        db.session.add(user)
        db.session.commit()
        
        subject = "Please confirm your email"
        html = 'email/activate.html'

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)

        data = {
            "confirm_url":confirm_url
        }


        send_email(user.email, subject, html, data)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for("auth.unconfirmed"))

    return render_template('auth/register.html', form=form)


@mod_auth.route('/confirm/<token>')
@mobile_template('{mobile/}public/index.html')
@login_required
def confirm_email(template,token):
    if current_user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
        return render_template(template)
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return render_template(template)


@mod_auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.home')
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('auth/login.html', form=form)
    return render_template('auth/login.html', form=form)


@mod_auth.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))


@mod_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.login'))

