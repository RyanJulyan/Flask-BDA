
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_required

# Import the database object from the main app module
from app import db, app

# Import module forms
from app.mod_xyz.forms import XyzForm

# Import module models (e.g. User)
from app.mod_xyz.models import Xyz

# Define the blueprint: 'xyz', set its url prefix: app.url/xyz
mod_public_xyz = Blueprint('xyz_public', __name__, url_prefix='/xyz')
mod_admin_xyz = Blueprint('xyz_admin', __name__, url_prefix='/admin/xyz')

# If in form is submitted
form = XyzForm(request.form)


# Set the route and accepted methods
@mod_public_xyz.route('/', methods=['GET'])
def public_list():
    page = request.args.get('page', 1, type=int)
    data = Xyz.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template("xyz/public/public_list.html", data=data)


@mod_admin_xyz.route('/', methods=['GET'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    data = Xyz.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template("xyz/admin/index.html", data=data)


@mod_admin_xyz.route('/create', methods=['GET'])
@login_required
def create():

    return render_template("xyz/admin/create.html", form=form)


@mod_admin_xyz.route('/store', methods=['POST'])
@login_required
def store():
    data = Xyz(
        # start new request feilds
        # this line should be removed and replaced with the newFormRequestDefinitions variable
        # end new request feilds
        # title=request.form.get("title")
    )
    db.session.add(data)
    db.session.commit()

    return redirect(url_for('xyz_admin.index'))


@mod_admin_xyz.route('/show/<id>', methods=['GET'])
@login_required
def show(id):
    data = Xyz.query.get(id)

    return render_template("xyz/admin/show.html", data=data)


@mod_admin_xyz.route('/edit/<id>', methods=['GET'])
@login_required
def edit(id):
    data = Xyz.query.get(id)

    return render_template("xyz/admin/edit.html", form=form, data=data)


@mod_admin_xyz.route('/update/<id>', methods=['PUT', 'PATCH'])
@login_required
def update(id):
    data = Xyz.query.get(id)
    # start update request feilds
    # this line should be removed and replaced with the updateFormRequestDefinitions variable
    # end update request feilds
    # data.title = request.form.get("title")
    db.session.commit()

    return redirect(url_for('xyz_admin.index'))


@mod_admin_xyz.route('/destroy/<id>', methods=['POST', 'DELETE'])
@login_required
def destroy(id):
    data = Xyz.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('xyz_admin.index'))
