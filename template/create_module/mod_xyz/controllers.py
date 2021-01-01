
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_xyz.forms import XyzForm

# Import module models (i.e. User)
from app.mod_xyz.models import Xyz

# Define the blueprint: 'xyz', set its url prefix: app.url/xyz
mod_public_xyz = Blueprint('xyz_public', __name__, url_prefix='/xyz')
mod_admin_xyz = Blueprint('xyz_admin', __name__, url_prefix='/admin/xyz')

# Set the route and accepted methods
@mod_public_xyz.route('/', methods=['GET'])
def public_list():
  data = {}
  data['xyz'] = Xyz.query.all()
  
  return render_template("xyz/public/public_list.html", data=data)

@mod_admin_xyz.route('/', methods=['GET'])
def index():
  data = {}
  data['xyz'] = Xyz.query.all()
  
  return render_template("xyz/admin/index.html", data=data)

@mod_admin_xyz.route('/create', methods=['GET'])
def create():
  data = {}

  return render_template("xyz/admin/create.html", data=data)

@mod_admin_xyz.route('/store', methods=['POST'])
def store():

  data = Xyz(
      # new request feilds
      # title=request.form.get("title")
  )

  return redirect(url_for('xyz_admin.index'))

@mod_admin_xyz.route('/show/<id>', methods=['GET'])
def show(id):
  data = {}
  data['xyz'] = Xyz.query.get(id)
  
  return render_template("xyz/admin/show.html", data=data)

@mod_admin_xyz.route('/edit/<id>', methods=['GET'])
def edit(id):
  data = {}
  data['xyz'] = Xyz.query.get(id)
  
  return render_template("xyz/admin/edit.html", data=data)

@mod_admin_xyz.route('/update/<id>', methods=['PUT','PATCH'])
def update(id):
  data = {}
  # data['xyz'] = Xyz.query.filter_by(email=form.email.data).first()
  
  return redirect(url_for('xyz_admin.index'))

@mod_admin_xyz.route('/destroy/<id>', methods=['POST','DELETE'])
def destroy(id):
  data = {}
  # data['xyz'] = Xyz.query.filter_by(email=form.email.data).first()
  
  return redirect(url_for('xyz_admin.index'))