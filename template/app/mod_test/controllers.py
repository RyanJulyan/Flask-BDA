
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Import module forms
# from app.mod_test.forms import LoginForm

# Import module models (i.e. User)
from app.mod_test.models import Test

# Define the blueprint: 'test', set its url prefix: app.url/test
mod_public_test = Blueprint('test_public', __name__, url_prefix='/test')
mod_admin_test = Blueprint('test_admin', __name__, url_prefix='/admin/test')

# Set the route and accepted methods
@mod_public_test.route('/', methods=['GET'])
def public_list():
  data = {}
  data['test'] = Test.query.all()
  
  return render_template("test/public/public_list.html", data=data)

@mod_admin_test.route('/', methods=['GET'])
def index():
  data = {}
  data['test'] = Test.query.all()
  
  return render_template("test/admin/index.html", data=data)

@mod_admin_test.route('/create', methods=['GET'])
def create():
  data = {}

  return render_template("test/admin/create.html", data=data)

@mod_admin_test.route('/store', methods=['POST'])
def store():

  data = Test(
      # new request feilds
      # title=request.form.get("title")
  )

  return redirect(url_for('test_admin.index'))

@mod_admin_test.route('/show/<id>', methods=['GET'])
def show(id):
  data = {}
  data['test'] = Test.query.get(id)
  
  return render_template("test/admin/show.html", data=data)

@mod_admin_test.route('/edit/<id>', methods=['GET'])
def edit(id):
  data = {}
  data['test'] = Test.query.get(id)
  
  return render_template("test/admin/edit.html", data=data)

@mod_admin_test.route('/update/<id>', methods=['PUT','PATCH'])
def update(id):
  data = {}
  # data['test'] = Test.query.filter_by(email=form.email.data).first()
  
  return redirect(url_for('test_admin.index'))

@mod_admin_test.route('/destroy/<id>', methods=['POST','DELETE'])
def destroy(id):
  data = {}
  # data['test'] = Test.query.filter_by(email=form.email.data).first()
  
  return redirect(url_for('test_admin.index'))