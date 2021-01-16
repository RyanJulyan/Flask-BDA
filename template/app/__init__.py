
# Import flask and template operators
from flask import Flask, render_template, make_response, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

# flask-debugtoolbar
from flask_debugtoolbar import DebugToolbarExtension

# flask-mobility specific mobile views
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template

# Import Flask API and Resource from Swagger for API
from flask_restful_swagger_3 import Resource, Api

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
api = Api(app)
Mobility(app)

# Login_manager
login_manager = LoginManager()
login_manager.init_app(app)

# Configurations
app.config.from_object('config')
# Debug Toolbar
toolbar = DebugToolbarExtension(app)

# Serializer
serializer = URLSafeTimedSerializer(app.secret_key)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Import module models (i.e. User)
from app.mod_auth.models import User  # noqa: E402


# User_loader
@login_manager.user_loader
def load_user(session_token):
    user = User.query.filter_by(session_token=session_token).first()

    try:
        serializer.loads(session_token, max_age=app.config['TIME_TO_EXPIRE'])
    except SignatureExpired:
        user.session_token = None
        db.session.commit()
        return None

    return user


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('./404.html'), 404


@app.errorhandler(403)
def not_allowed(error):
    return render_template('./403.html'), 403


# Serve Service Worker
@app.route('/sw.js')
def sw():
    response = make_response(send_from_directory('static', filename='sw.js'))
    # change the content header file
    response.headers['Content-Type'] = 'application/javascript'
    return response
    # return app.send_static_file('sw.js')


# Serve Landing Page
@app.route('/')
@mobile_template('{mobile/}public/index.html')
def landing(template):
    return render_template(template)


# Import a module / component using its blueprint handler variable (mod_auth)
# from app.mod_xyz.controllers import mod_xyz as xyz_module
from app.mod_auth.controllers import mod_auth as auth_module  # noqa: E402
# import new xyz_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# register_blueprint new xyz_module

# Register api(s)
# new xyz api resource routing

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
