
# Import flask and template operators
from flask import Flask, render_template, make_response, send_from_directory, request, g
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_wtf.csrf import CSRFProtect

# Import logging
import logging

# Rate limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# flask-debugtoolbar
from flask_debugtoolbar import DebugToolbarExtension

# flask-mobility specific mobile views
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template

# Import Flask API and Resource from Swagger for API
from flask_restx import Api, Resource
from flask_cors import CORS

# JWT for API
from flask_jwt_extended import JWTManager, create_access_token

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from app.mod_tenancy.multi_tenant import MultiTenantSQLAlchemy

# Import Mail
from flask_mail import Mail

# Import SocketIO
from flask_socketio import SocketIO
from engineio.async_drivers import gevent

# Import Bcrypt
from flask_bcrypt import Bcrypt

# Import APScheduler
from flask_apscheduler import APScheduler
from apscheduler.events import (
    EVENT_JOB_ADDED,
    EVENT_JOB_ERROR,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MISSED,
    EVENT_JOB_REMOVED,
    EVENT_JOB_SUBMITTED,
)

# Define the WSGI application object
app = Flask(__name__, template_folder='templates')
Mobility(app)

# JWT
jwt = JWTManager(app)
jwt.init_app(app)

# Login_manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = "danger"

# Configurations
app.config.from_object('config')

# Logging
logging.basicConfig(filename=app.config['LOG_FILENAME'], level=app.config['LOG_LEVEL'], format=app.config['LOG_FORMAT'])

# Rate Limit
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=app.config['DEFAULT_LIMITS']
)

# CORS
CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

# Cross-site request forgery (Csrf) Protection
csrf_protect = CSRFProtect(app)

# Debug Toolbar
toolbar = DebugToolbarExtension(app)

# Serializer
serializer = URLSafeTimedSerializer(app.secret_key)

# Define the database object which is imported
# by modules and controllers
db = MultiTenantSQLAlchemy(app)

# SocketIO
socketio = SocketIO(app)

# Bcrypt
bcrypt = Bcrypt(app)

# Mail
mail = Mail(app)

# JWT blacklist 
blacklist = set()

# initialize scheduler
scheduler = APScheduler()
def job_missed(event):
    """Job missed event."""
    with scheduler.app.app_context():
        app.logger.warning('Job missed for organisation: ' + g.organization + '. Event details: ' + event)


def job_error(event):
    """Job error event."""
    with scheduler.app.app_context():
        app.logger.error('Job error for organisation: ' + g.organization + '. Event details: ' + event)


def job_executed(event):
    """Job executed event."""
    with scheduler.app.app_context():
        app.logger.info('Job executed for organisation: ' + g.organization + '. Event details: ' + event)


def job_added(event):
    """Job added event."""
    with scheduler.app.app_context():
        app.logger.info('Job added for organisation: ' + g.organization + '. Event details: ' + event)


def job_removed(event):
    """Job removed event."""
    with scheduler.app.app_context():
        app.logger.info('Job removed for organisation: ' + g.organization + '. Event details: ' + event)


def job_submitted(event):
    """Job scheduled to run event."""
    with scheduler.app.app_context():
        app.logger.info('Job scheduled to run for organisation: ' + g.organization + '. Event details: ' + event)


scheduler.add_listener(job_missed, EVENT_JOB_MISSED)
scheduler.add_listener(job_error, EVENT_JOB_ERROR)
scheduler.add_listener(job_executed, EVENT_JOB_EXECUTED)
scheduler.add_listener(job_added, EVENT_JOB_ADDED)
scheduler.add_listener(job_removed, EVENT_JOB_REMOVED)
scheduler.add_listener(job_submitted, EVENT_JOB_SUBMITTED)

scheduler.init_app(app)
scheduler.start()

# Import module models (i.e. User)
from app.mod_auth.models import User  # noqa: E402
from app.mod_api_keys.models import Api_keys  # noqa: E402

@app.before_request
def before_request():
    # Just use the query parameter "tenant"
    # organization = tenant
    g.organization = "default"
    if 'organization' in request.args:
        g.organization = request.args['organization']
        app.logger.info('Organisation changed: '+ g.organization)

    # Set database to tenant
    db.choose_tenant(g.organization)

    # Set User JWT token if API key Used
    if("ApiKey" in request.headers):
        ApiKey = request.headers.get('ApiKey')
        # api_key = Api_keys.query.filter_by(_and(api_key = ApiKey,and_(Api_keys.birthday <= '1988-01-17', Api_keys.birthday >= '1985-01-17'))).first()
        api_key = Api_keys.query.filter_by(api_key = ApiKey).first()
        data = User.query.get_or_404(api_key.created_user_id)

        # request.headers['Authorization'] = "Bearer "+ create_access_token(identity=data.email)
        if api_key:
            request.headers['Authorization'] = "Bearer "+ create_access_token(identity=ApiKey)

    # Build the database:
    # This will create the database file using SQLAlchemy
    db.create_all()


# User_loader
@login_manager.user_loader
def load_user(_user_id):
    return User.query.get_or_404(_user_id)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    app.logger.warning('Organisation error 404 for: '+ g.organization)
    return render_template('./errors/404.html'), 404


@app.errorhandler(403)
def not_allowed(error):
    app.logger.error('Organisation error 403 for: '+ g.organization)
    return render_template('./errors/403.html'), 403


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.warning('Organisation error 500 for: '+ g.organization)
    return render_template('./errors/500.html'), 500


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
# api_keys
from app.mod_api_keys.controllers import mod_public_api_keys as api_keys_public_module  # noqa: E402
from app.mod_api_keys.controllers import mod_admin_api_keys as api_keys_admin_module  # noqa: E402
# hierarchies
from app.mod_hierarchies.controllers import mod_public_hierarchies as hierarchies_public_module  # noqa: E402
from app.mod_hierarchies.controllers import mod_admin_hierarchies as hierarchies_admin_module  # noqa: E402
# organisations
from app.mod_organisations.controllers import mod_public_organisations as organisations_public_module  # noqa: E402
from app.mod_organisations.controllers import mod_admin_organisations as organisations_admin_module  # noqa: E402

# Register blueprint(s)
app.register_blueprint(auth_module)
# register_blueprint new xyz_module
# api_keys
app.register_blueprint(api_keys_public_module)
app.register_blueprint(api_keys_admin_module)
# hierarchies
app.register_blueprint(hierarchies_public_module)
app.register_blueprint(hierarchies_admin_module)
# organisations
app.register_blueprint(organisations_public_module)
app.register_blueprint(organisations_admin_module)


# Define the API
# This must be after other routes or it overwrites everything.
authorizations = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'ApiKey'
    }
}
api = Api(app, version='3.0',
    title=app.config['SITE_TITLE'] + ' API',
    description=app.config['SITE_DESCRIPTION'] + ' API',
    # base_url='/api',  # this did not work when set so moved to docs
    doc=app.config['SWAGGER_URL'],
    security=['jwt','apikey'],
    decorators=[csrf_protect.exempt],
    authorizations=authorizations
)


# Register api(s)
from app.mod_auth.api_controllers import ns as Auth_API  # noqa: E402
# new xyz api resources
# api_keys
from app.mod_api_keys.api_controllers import ns as Api_keys_API  # noqa: E402
# hierarchies
from app.mod_hierarchies.api_controllers import ns as Hierarchies_API  # noqa: E402
# organisations
from app.mod_organisations.api_controllers import ns as Organisations_API  # noqa: E402


# This MUST be the last route to allow for all API routes to be registered
# Serve API to Postman collection
@app.route('/api/postman')
def postman():
    urlvars = True  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    return data
