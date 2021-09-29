
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
from app import db, app, bcrypt

# Import module forms
from app.mod_users.forms import LoginForm, RegisterForm, ChangePasswordForm, ForgotForm

# Import module models (i.e. Users)
from app.mod_users.models import Users

# Import send_email
from app.mod_email.controllers import send_email

# Define the blueprint: 'users', set its url prefix: app.url/users
mod_users = Blueprint('users', __name__, template_folder='templates', url_prefix = '/users')


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('users.unconfirmed'))
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
@mod_users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    
    if form.validate_on_submit():
        user = Users(
            name = form.name.data,
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
        confirm_url = url_for('users.confirm_email', token=token, _external=True)+"?organization="+g.organization

        data = {
            "confirm_url":confirm_url
        }


        send_email(user.email, subject, html, data)
        # send_email(user.email, subject, html_template, data)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for("users.unconfirmed"))

    return render_template('users/register.html', form=form)


@mod_users.route('/confirm/<token>')
@mobile_template('{mobile/}public/index.html')
@login_required
def confirm_email(template,token):
    if current_user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
        return render_template(template)
    email = confirm_token(token)
    user = Users.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return render_template(template)


@mod_users.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.home')
    flash('Please confirm your account!', 'warning')
    return render_template('users/unconfirmed.html')


@mod_users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            
            login_user(user,remember=True)
            session['_user_id'] = user.id 

            flash('Welcome.', 'success')
            
            next = request.args.get('next')

            return redirect(next or url_for('users_admin.index'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('users/login.html', form=form)
    return render_template('users/login.html', form=form)


@mod_users.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = render_template('users/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('users.unconfirmed'))


@mod_users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('users.login'))


@mod_users.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('users/forgot.html', form=form)

