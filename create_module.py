# Python 3

##########################
##########################
######## Imports #########
##########################
##########################
import os
import shutil
import re

##################################
##################################
######## Project Details #########
##################################
##################################
def getBool(prompt):
  while True:
    try:
      return {"true":True,"false":False}[input(prompt).lower()]
    except KeyError:
      print ("Invalid input please enter True or False!")

def getStringNum(prompt):
  while True:
    try:
        num = int(input(prompt))
        if(num < 1 or num > 256):
          return getStringNum("That's not a valid number between 1-256!\n"+prompt)
        return num
    except:
        print("That's not a valid number between 1-256!")

def getDataType(prompt):
  while True:
    try:
      return {
        "string":"String",
        "int":"Integer",
        "float":"Numeric(38, 19)",
        "numeric":"Numeric(38, 19)",
        "text":"Text",
        "date":"Date",
        "datetime":"DateTime",
        "boolean":"Boolean",
        "bigint":"BigInteger",
        "enum":"Enum",
        "json":"JSON",
        "largebinary":"LargeBinary"
      }[input(prompt).lower()]
    except KeyError:
      print ("Invalid data type")

def module():
  print("Module Name: ")
  while True:
    module = input()
    if(len(module) > 0):
      module = module.casefold()
      module = re.sub('[;!,*)@#%(&$?.^\'"+<>/\\{}]', '', module)
      module = module.replace(" ", "_")
      return module
    else:  
      print("Invalid Module Name!")
      print("Please enter a valid module name:")

def getEnumParameters():
  parameters = []
  while True:
    field = input("Create new Parameter Value (type the string: 'STOP_CREATING_PARAMETERS' to exit): ")
    if(field == 'STOP_CREATING_PARAMETERS'):
      return parameters
    if(field in parameters):
      print("Parameter Value Already Exists!")
      print("Please enter a different parameter value!")
    elif(len(field) > 0):
      parameters.append(field)
    else:  
      print("Invalid Parameter Value!")
      print("Please enter a valid parameter value!")

def fields():
  fields = {}
  while True:
    print("Create new field Name (type the string: 'STOP_CREATING_FIELDS' to exit): ")
    field = input()
    if(field == 'STOP_CREATING_FIELDS'):
      return fields
    if(field in fields):
      print("Field Name Already Exists!")
      print("Please enter a different field name!")
    elif(len(field) > 0):
      field = field.casefold()
      field = re.sub('[;!,*)@#%(&$?.^\'"+<>/\\{}]', '', field)
      field = field.replace(" ", "_")
      dataType = getDataType("What datatype is " + field + """
        'String'
        'Int'
        'Float'
        'Numeric'
        'Text'
        'Date'
        'DateTime'
        'Boolean'
        'BigInt'
        'Enum'
        'JSON'
        'LargeBinary': """)
      if(dataType == 'String'):
        num = getStringNum("String Length (1-256):")
        dataType = "String(" + str(num) + ")"
      if(dataType == 'Enum'):
        parameters = getEnumParameters()
        dataType = "Enum(" + str((', '.join('"' + item + '"' for item in parameters))) + ")"
      nullable = getBool("is " + field + " nullable ('True', 'False'): ")
      unique = getBool("is " + field + " unique ('True', 'False'): ")
      default = input("Default value: ") or False
      fields[field] = {
        "dataType":dataType,
        "nullable":nullable,
        "unique":unique,
        "default":default
      }
    else:  
      print("Invalid Field Name!")
      print("Please enter a valid field name:")

# Prompt user 
module = module()
model = module.capitalize()
fields = fields()

# process user data
columns = '  \n'
feildNames = []
instanceNames = '    \n'
instanceParams = ''

for key, value in fields.items():
  columns += "  {} = db.Column(db.{}, nullable={},default={}, unique={})\n".format(key,value['dataType'],value['nullable'],value['default'],value['unique'])
  instanceNames += "    self.{} = {}\n".format(key,key)
  feildNames.append(key)

instanceParams = str((', '.join( item for item in feildNames)))

########################################
########################################
######## Make Base Directories #########
########################################
########################################
os.system('mkdir "app/mod_' + module +'"')
os.system('mkdir "app/templates/' + module + '"')

################################################
################################################
######## Creating A Module / Component #########
################################################
################################################

############################
############################
######## mod_ Init #########
############################
############################

########################################################################
######## Copy App __init__.py for manage source -> destination #########
########################################################################

shutil.copy2('app/__init__.py', 'app/__init__.py~')

###############################################
######## manage source -> destination #########
###############################################

destination= open('app/__init__.py', "w" )
source = open('app/__init__.py~', "r" )

for line in source:
    
    destination.write( line )
    
    if "# import new xyz_module" in line:
        destination.write("from app.mod_" + module + ".controllers import mod_" + module + " as " + module + "_module\n" )
    
    if "# register_blueprint new xyz_module" in line:
        destination.write("app.register_blueprint(" + module + "_module)\n" )

source.close()
destination.close()

################################
######## remove source #########
################################
os.remove('app/__init__.py~')

###################################
######## mod_ controllers #########
###################################
f = open('app/mod_' + module +'/controllers.py', "w")
f.write("""
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_""" + module +""".forms import LoginForm

# Import module models (i.e. User)
from app.mod_""" + module +""".models import """ + model +"""

# Define the blueprint: '""" + module +"""', set its url prefix: app.url/""" + module +"""
mod_""" + module +""" = Blueprint('""" + module +"""', __name__, url_prefix='/""" + module +"""')

# Set the route and accepted methods
@mod_""" + module +""".route('/', methods=['GET'])
def index():
  data = {}
  data['""" + module +"""'] = """ + model +""".query.all()
  
  return render_template(\""""+ module +"""/index.html\", data=data)

@mod_""" + module +""".route('/create/', methods=['GET'])
def create():
  data = {}

  return render_template(\""""+ module +"""/create.html\", data=data)

@mod_""" + module +""".route('/store/', methods=['POST'])
def store():

  post = """ + model +"""(
      title=request.form.get("title"),
      body=request.form.get("body"),
      author_id = g.user.id,
      slug = slugify(request.form.get("title"))
  )

  return redirect(url_for('""" + module +""".index'))

@mod_""" + module +""".route('/show/<id>', methods=['GET'])
def show(id):
  data = {}
  data['""" + module +"""'] = """ + model +""".query.get(id=form.id.data)
  
  return render_template(\""""+ module +"""/show.html\", data=data)

@mod_""" + module +""".route('/edit/<id>', methods=['GET'])
def edit(id):
  data = {}
  data['""" + module +"""'] = """ + model +""".query.get(id=form.id.data)
  
  return render_template(\""""+ module +"""/edit.html\", data=data)

@mod_""" + module +""".route('/update/<id>', methods=['PUT','PATCH'])
def update(id):
  data = {}
  data['""" + module +"""'] = """ + model +""".query.filter_by(email=form.email.data).first()
  
  return redirect(url_for('""" + module +""".show'))

@mod_""" + module +""".route('/destroy/<id>', methods=['POST'])
def destroy(id):
  data = {}
  data['""" + module +"""'] = """ + model +""".query.filter_by(email=form.email.data).first()
  
  return redirect(url_for('""" + module +""".index'))

""")
f.close()

##############################
######## mod_ models #########
##############################
f = open('app/mod_' + module +'/models.py', "w")
f.write("""
# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  
  __abstract__  = True
  id            = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
  created_at    = db.Column(db.DateTime, default=db.func.current_timestamp())
  updated_at    = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
  deleted_at    = db.Column(db.DateTime, nullable=True)

# Define a """+ model + """ model
class """+ model + """(Base):
  __tablename__ = '""" + module +"""'
  # Fields
  """+ columns + """
  # New instance instantiation procedure
  def __init__(self, """ + instanceParams + """):
    """ + instanceNames + """
    self.deleted_at = deleted_at
  
  def __repr__(self):
    return '<"""+ model + """ %r>' % (self.name)
""")
f.close()

#############################
######## mod_ forms #########
#############################
f = open('app/mod_' + module +'/forms.py', "w")
f.write("""
# Import Form and RecaptchaField (optional)
from flask_wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, BooleanField

# Import Form validators
from wtforms.validators import Required

# Define the login form (WTForms)

class LoginForm(Form):
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])
""")
f.close()

##################################
######## mod_ index.html #########
##################################
f = open('app/templates/' + module +'/index.html', "w")
f.write("""
{% extends "index.html" %}

{% block content %}

{% endblock content %}
""")
f.close()
###################################
######## mod_ create.html #########
###################################
f = open('app/templates/' + module +'/create.html', "w")
f.write("""
{% extends "index.html" %}

{% block content %}

{% endblock content %}
""")
f.close()
#################################
######## mod_ show.html #########
#################################
f = open('app/templates/' + module +'/show.html', "w")
f.write("""
{% extends "index.html" %}

{% block content %}

{% endblock content %}
""")
f.close()
#################################
######## mod_ edit.html #########
#################################
f = open('app/templates/' + module +'/edit.html', "w")
f.write("""
{% extends "index.html" %}

{% block content %}

{% endblock content %}
""")
f.close()


