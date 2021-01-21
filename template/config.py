
import os

SITE_TITLE = 'Flask-BDA'
SITE_URL = 'http://www.Flask-BDA.com'
SITE_DESCRIPTION = 'My awesome new Flask-BDA site.'
SITE_THEME_COLOR = '#3367D6'
DEVELOPER_NAME = 'Ryan Julyan'

# Statement for enabling the development environment
DEBUG = True
DEBUG_TB_PROFILER_ENABLED = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database engine - we are working with
# SQLite for this example
DATABASE_ENGINE = 'sqlite:///'

# MySQL
# DATABASE_ENGINE = 'mysql://'

# PostgreSQL
# DATABASE_ENGINE = 'postgresql://'

# SQLServer
# DATABASE_ENGINE = 'mssql+pymssql://'
# TRUSTED_CONNECTION = 'yes'  # for windows authentication.

DATABASE_HOST = ''
DATABASE_PORT = ''
DATABASE_USERNAME = ''
DATABASE_PASSWORD = ''
DATABASE_NAME = os.path.join(BASE_DIR, 'app.db')


# Amazon DynamoDB
# DATABASE_ENGINE = 'amazondynamodb///?'
# DYNAMODB_ACCESS_KEY = ''
# DYNAMODB_SECRET_KEY = ''
# DYNAMODB_DOMAIN = 'amazonaws.com'
# DYNAMODB_REGION = 'us-east-1'

SQLALCHEMY_DATABASE_URI = DATABASE_ENGINE + DATABASE_HOST + DATABASE_PORT + DATABASE_NAME

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Time for session expirey
TIME_TO_EXPIRE = 3600

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True
# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = 'secret'

# Secret key for signing cookies
SECRET_KEY = 'secret'

# Secret key for signing JWT (JSON Web Tokens)
JWT_SECRET_KEY = 'secret'

# Default number of results to show per page
ROWS_PER_PAGE = 20

# Email Credentails
MAIL_MAILER = 'smtp'
MAIL_HOST = 'smtp.mailtrap.io'
MAIL_PORT = 2525
MAIL_USERNAME = 'email@example.com'
MAIL_PASSWORD = 'example password'
MAIL_ENCRYPTION = None
MAIL_FROM_ADDRESS = 'email@example.com'
MAIL_FROM_NAME = 'Flask-BDA'

# Swagger
SWAGGER_BLUEPRINT_URL_PREFIX = '/swagger'
SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
SWAGGER_API_URL = 'swagger.json'  # Our API url (can of course be a local resource)

# Search Engine Optimization (SEO)
SEO_SUBJECT = 'Rapid Application Development.'
SEO_SUBTITLE = 'Flask-BDA Site.'
SEO_SUMMARY = 'This site was created using Flask-BDA.'
SEO_ABSTRACT = 'This site was created using Flask-BDA.'
SEO_KEYWORDS = 'Flask, PWA, Python, Rapid Application Development, RAD, Progressive Web App, Flask-BDA.'
SEO_REVISIT_AFTER = '7 days'
