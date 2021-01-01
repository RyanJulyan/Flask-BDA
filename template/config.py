

SITE_TITLE = 'Flask BDA'
SITE_URL = 'http://www.bda.com'
SITE_DESCRIPTION = 'My awesome new Flask BDA site.'
SITE_THEME_COLOR = '#3367D6'
DEVELOPER_NAME = 'Ryan Julyan'

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
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

# Email Credentails
MAIL_MAILER='smtp'
MAIL_HOST='smtp.mailtrap.io'
MAIL_PORT=2525
MAIL_USERNAME='email@example.com'
MAIL_PASSWORD='example password'
MAIL_ENCRYPTION=None
MAIL_FROM_ADDRESS='email@example.com'
MAIL_FROM_NAME='Flask BDA'

# Search Engine Optimization (SEO)
SEO_SUBJECT = 'Rapid Application Development.'
SEO_SUBTITLE = 'Flask BDA Site.'
SEO_SUMMARY = 'This site was created using Flask BDA.'
SEO_ABSTRACT = 'This site was created using Flask BDA.'
SEO_KEYWORDS = 'Flask, PWA, Python, Rapid Application Development, RAD, Progressive Web App, Flask BDA.'
SEO_REVISIT_AFTER = '7 days'

