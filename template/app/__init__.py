
# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('./404.html'), 404
@app.errorhandler(403)
def not_found(error):
    return render_template('./403.html'), 403

#Serve Service Worker
@app.route('/sw.js')
def sw():
    response = make_response(send_from_directory('static', filename='sw.js'))
    #change the content header file
    response.headers['Content-Type']='application/javascript'
    return response
    # return app.send_static_file('sw.js')

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
# import new xyz_module
from app.mod_xyz.controllers import mod_xyz as xyz_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# register_blueprint new xyz_module
app.register_blueprint(xyz_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
