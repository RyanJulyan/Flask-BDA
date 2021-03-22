
# Import flask and template operators
from flask import Flask, render_template, make_response, send_from_directory, request, g
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_wtf.csrf import CSRFProtect

# flask-debugtoolbar
from flask_debugtoolbar import DebugToolbarExtension

# flask-mobility specific mobile views
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template

# Import Flask API and Resource from Swagger for API
from flask_restx import Api, Resource
from flask_cors import CORS

# JWT for API
from flask_jwt_extended import JWTManager

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from app.mod_tenancy.multi_tenant import MultiTenantSQLAlchemy

# Import Mail
from flask_mail import Mail

# Import SocketIO
from flask_socketio import SocketIO

# Define the WSGI application object
app = Flask(__name__)
Mobility(app)

# JWT
jwt = JWTManager(app)
jwt.init_app(app)

# Login_manager
login_manager = LoginManager()
login_manager.init_app(app)

# Configurations
app.config.from_object('config')

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

@app.before_request
def before_request():
    # Just use the query parameter "tenant"
    # organization = tenant
    g.organization = "core"
    if 'organization' in request.args:
        g.organization = request.args['organization']

    # Set database to tenant
    db.choose_tenant(g.organization)

    # Build the database:
    # This will create the database file using SQLAlchemy
    db.create_all()

# Mail
mail = Mail(app)

# JWT blacklist 
blacklist = set()

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
    return render_template('./errors/404.html'), 404


@app.errorhandler(403)
def not_allowed(error):
    return render_template('./errors/403.html'), 403


@app.errorhandler(500)
def internal_server_error(error):
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
# organisations
from app.mod_organisations.controllers import mod_public_organisations as organisations_public_module  # noqa: E402
from app.mod_organisations.controllers import mod_admin_organisations as organisations_admin_module  # noqa: E402

# Register blueprint(s)
app.register_blueprint(auth_module)
# register_blueprint new xyz_module
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
    }
}
api = Api(app, version='1.0',
    title=app.config['SITE_TITLE'] + ' API',
    description=app.config['SITE_DESCRIPTION'] + ' API',
    # base_url='/api',  # this did not work when set so moved to docs
    doc=app.config['SWAGGER_URL'],
    security='jwt',
    decorators=[csrf_protect.exempt],
    authorizations=authorizations
)


# Register api(s)
from app.mod_auth.api_controllers import ns as Auth_API  # noqa: E402
# new xyz api resources
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
