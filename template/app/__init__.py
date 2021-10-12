
import sys, os

from datetime import date

# Import flask and template operators
from flask import Flask, render_template, make_response, send_from_directory, request, g, jsonify, redirect, url_for
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

# Import request for API calls 
import requests

# Import json for consuming payload and for payload data type transformations
import json

# Import GraphQLAuth
# from flask_graphql_auth import GraphQLAuth

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

# Login_manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = "danger"

# Configurations
# app.config.from_object('config') # Removed to allow for external config file

# Load Config depending on where it comes from
if getattr(sys, 'frozen', False):
    # running as bundle (aka frozen)
    # bundle_dir = sys._MEIPASS
    # application_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    bundle_dir = os.path.dirname(sys.executable)
else:
    # running live
    bundle_dir = os.path.dirname(os.path.join(os.path.dirname( __file__ ), '..','..'))

app.config.from_pyfile(os.path.join(bundle_dir, 'config.py'))

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

# GraphQLAuth
# graph_ql_auth = GraphQLAuth(app)

# JWT
jwt = JWTManager(app)
jwt.init_app(app)

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

# Import module models (i.e. Users)
from app.mod_users.models import Users  # noqa: E402
from app.mod_organisations.models import Organisations  # noqa: E402
from app.mod_api_keys.models import Api_keys  # noqa: E402


#################################################################################
## NOT GOOD, CHANGES THE SERVER TO ALWAYS HAVE AUTH AND NOT JUST SINGLE REQUEST##
#################################################################################
# BearerToken = ''

# class InterceptRequestMiddleware:
#     global BearerToken
#     def __init__(self, wsgi_app):
#         self.wsgi_app = wsgi_app

#     def __call__(self, environ, start_response):
#         global BearerToken
#         # print("BearerToken: ",BearerToken)
#         environ['HTTP_AUTHORIZATION'] = BearerToken
#         return self.wsgi_app(environ, start_response)

# app.wsgi_app = InterceptRequestMiddleware(app.wsgi_app)
#################################################################################
## NOT GOOD, CHANGES THE SERVER TO ALWAYS HAVE AUTH AND NOT JUST SINGLE REQUEST##
#################################################################################

# @app.before_first_request
# def before_first_request():
#     global BearerToken
#     BearerToken = ''

@app.before_request
def before_request():
    # Just use the query parameter "?organization=tenant_name"
    # organization = tenant
    g.organization = "default"
    if 'organization' in request.args:
        g.organization = request.args['organization']
        app.logger.info('Organisation changed: '+ g.organization)

    # Set database to tenant
    db.choose_tenant(g.organization)
            

    # Build the database:
    if app.config['AUTO_CREATE_TABLES_FROM_MODELS']:
        # This will create the database tables using SQLAlchemy
        db.create_all()

    # print('-------------------------------')
    # print('-------------------------------')
    # print('-------------------------------')
    # print('Keys:', db.session.execute(Users.query).keys())
    # print('-------------------------------')
    # print('-------------------------------')
    # print('-------------------------------')
    
    g.organisation_id = 1
    organisation = Organisations.query.filter(Organisations.organisation_name == g.organization).first()

    if organisation:
        g.organisation_id = organisation.id

    # Set User JWT token if API key Used
    if("ApiKey" in request.headers):
        ApiKey = request.headers.get('ApiKey')
        current_date =date.today()

        api_key = Api_keys.query.filter(Api_keys.api_key == ApiKey).filter(Api_keys.valid_from <= current_date).filter(current_date <= Api_keys.valid_to).first()

        if api_key:
            BearerToken = "Bearer " + create_access_token(identity=ApiKey)

            params = request.args
            headers = dict(request.headers)
            headers['Authorization'] = BearerToken
            data = request.data.decode("UTF-8")
            if len(data) > 0:
                data = json.loads(data)

            if(request.method == 'GET'):

                url = request.url

                x = requests.get(url,params=params, headers=headers, json=data)

                # return_data = json.loads(x.text)

                # print("return_data: ", return_data)

            # if(request.method == 'post'):

            #     url = api_endpoint

            #     x = requests.post(url,params=params, headers=headers, json=data)

            #     data = json.loads(x.text)

            # if(request.method == 'put'):

            #     url = api_endpoint

            #     x = requests.put(url,params=params, headers=headers, json=data)

            #     data = json.loads(x.text)

            # if(request.method == 'delete'):

            #     url = api_endpoint

            #     x = requests.put(url,params=params, headers=headers, json=data)

            #     data = json.loads(x.text)


# make organisation accessable in template
@app.context_processor
def get_organization_in_template():
  return {
            "organization": g.organization,
            "organisation_id": g.organisation_id,
            "site_title": app.config['SITE_TITLE'],
            "site_url": app.config['SITE_URL']
        }

# @app.after_request
# def after_request(response):
#     print("response",dict(response))
#     return response

# @app.teardown_request
# def teardown_request(error=None):
#     global BearerToken
#     BearerToken = ''

@app.route('/header_check')
def index():
    return jsonify({'headers': {k: v for k, v in request.headers}})

# User_loader
@login_manager.user_loader
def load_user(_user_id):
    return Users.query.get_or_404(_user_id)


# Legal
@app.route('/legal/terms_of_use')
def terms_of_use():
    return render_template('./legal/terms_of_use.html')

@app.route('/legal/privacy_policy')
def privacy_policy():
    return render_template('./legal/privacy_policy.html')

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


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/seed/<int:level>")
def seed(level):
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if('seed' in url):
             links.append((url, rule.endpoint))
    return ' '.join([str(elem) for elem in links]) 
    # links is now a list of url, endpoint tuples

# Import a module / component using its blueprint handler variable (mod_users)
# site_settings
from app.mod_site_settings.controllers import mod_public_site_settings as site_settings_public_module  # noqa: E402
from app.mod_site_settings.controllers import mod_admin_site_settings as site_settings_admin_module  # noqa: E402
# organisations
from app.mod_organisations.controllers import mod_public_organisations as organisations_public_module  # noqa: E402
from app.mod_organisations.controllers import mod_admin_organisations as organisations_admin_module  # noqa: E402
# users
from app.mod_users.controllers import mod_users as users_module  # noqa: E402
# api_keys
from app.mod_api_keys.controllers import mod_public_api_keys as api_keys_public_module  # noqa: E402
from app.mod_api_keys.controllers import mod_admin_api_keys as api_keys_admin_module  # noqa: E402
# hierarchies
from app.mod_hierarchies.controllers import mod_public_hierarchies as hierarchies_public_module  # noqa: E402
from app.mod_hierarchies.controllers import mod_admin_hierarchies as hierarchies_admin_module  # noqa: E402
# cache_hierarchies
from app.mod_cache_hierarchies.controllers import mod_public_cache_hierarchies as cache_hierarchies_public_module  # noqa: E402
from app.mod_cache_hierarchies.controllers import mod_admin_cache_hierarchies as cache_hierarchies_admin_module  # noqa: E402
# calendar_periods
from app.mod_calendar_periods.controllers import mod_public_calendar_periods as calendar_periods_public_module  # noqa: E402
from app.mod_calendar_periods.controllers import mod_admin_calendar_periods as calendar_periods_admin_module  # noqa: E402
# calendar_definitions
from app.mod_calendar_definitions.controllers import mod_public_calendar_definitions as calendar_definitions_public_module  # noqa: E402
from app.mod_calendar_definitions.controllers import mod_admin_calendar_definitions as calendar_definitions_admin_module  # noqa: E402
# graphql
# from app.mod_graphql.controllers import mod_graphql as graphql_module  # noqa: E402
# from app.mod_xyz.controllers import mod_xyz as xyz_module
# import new xyz_module
# test
from app.mod_test.controllers import mod_public_test as test_public_module  # noqa: E402
from app.mod_test.controllers import mod_admin_test as test_admin_module  # noqa: E402
# test
from app.mod_test.controllers import mod_public_test as test_public_module  # noqa: E402
from app.mod_test.controllers import mod_admin_test as test_admin_module  # noqa: E402
# test
from app.mod_test.controllers import mod_public_test as test_public_module  # noqa: E402
from app.mod_test.controllers import mod_admin_test as test_admin_module  # noqa: E402
# test
from app.mod_test.controllers import mod_public_test as test_public_module  # noqa: E402
from app.mod_test.controllers import mod_admin_test as test_admin_module  # noqa: E402
# test
from app.mod_test.controllers import mod_public_test as test_public_module  # noqa: E402
from app.mod_test.controllers import mod_admin_test as test_admin_module  # noqa: E402
# test
from app.mod_test.controllers import mod_public_test as test_public_module  # noqa: E402
from app.mod_test.controllers import mod_admin_test as test_admin_module  # noqa: E402


# Register blueprint(s)
# site_settings
app.register_blueprint(site_settings_public_module)
app.register_blueprint(site_settings_admin_module)
# organisations
app.register_blueprint(organisations_public_module)
app.register_blueprint(organisations_admin_module)
# users
app.register_blueprint(users_module)
# api_keys
app.register_blueprint(api_keys_public_module)
app.register_blueprint(api_keys_admin_module)
# hierarchies
app.register_blueprint(hierarchies_public_module)
app.register_blueprint(hierarchies_admin_module)
# cache_hierarchies
app.register_blueprint(cache_hierarchies_public_module)
app.register_blueprint(cache_hierarchies_admin_module)
# calendar_periods
app.register_blueprint(calendar_periods_public_module)
app.register_blueprint(calendar_periods_admin_module)
# calendar_definitions
app.register_blueprint(calendar_definitions_public_module)
app.register_blueprint(calendar_definitions_admin_module)
# graphql
# app.register_blueprint(graphql_module)
# register_blueprint new xyz_module
# test
app.register_blueprint(test_public_module)
app.register_blueprint(test_admin_module)
# test
app.register_blueprint(test_public_module)
app.register_blueprint(test_admin_module)
# test
app.register_blueprint(test_public_module)
app.register_blueprint(test_admin_module)
# test
app.register_blueprint(test_public_module)
app.register_blueprint(test_admin_module)
# test
app.register_blueprint(test_public_module)
app.register_blueprint(test_admin_module)
# test
app.register_blueprint(test_public_module)
app.register_blueprint(test_admin_module)


# Prevent GraphQL The CSRF token is missing. error
# csrf_protect.exempt(graphql_module)

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
# site_settings
from app.mod_site_settings.api_controllers import ns as Site_settings_API  # noqa: E402
# organisations
from app.mod_organisations.api_controllers import ns as Organisations_API  # noqa: E402
# users
from app.mod_users.api_controllers import ns as User_API  # noqa: E402
# api_keys
from app.mod_api_keys.api_controllers import ns as Api_keys_API  # noqa: E402
# hierarchies
from app.mod_hierarchies.api_controllers import ns as Hierarchies_API  # noqa: E402
# cache_hierarchies
from app.mod_cache_hierarchies.api_controllers import ns as Cache_hierarchies_API  # noqa: E402
# calendar_definitions
from app.mod_calendar_definitions.api_controllers import ns as Calendar_definitions_API  # noqa: E402
# calendar_periods
from app.mod_calendar_periods.api_controllers import ns as Calendar_periods_API  # noqa: E402
# calendar_definitions
from app.mod_calendar_definitions.api_controllers import ns as Calendar_definitions_API  # noqa: E402
# new xyz api resources
# test
from app.mod_test.api_controllers import ns as Test_API  # noqa: E402
# test
from app.mod_test.api_controllers import ns as Test_API  # noqa: E402
# test
from app.mod_test.api_controllers import ns as Test_API  # noqa: E402
# test
from app.mod_test.api_controllers import ns as Test_API  # noqa: E402
# test
from app.mod_test.api_controllers import ns as Test_API  # noqa: E402
# test
from app.mod_test.api_controllers import ns as Test_API  # noqa: E402


# This MUST be the last route to allow for all API routes to be registered
# Serve API to Postman collection
@app.route('/api/postman')
def postman():
    urlvars = True  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    return data
