
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_required
from sqlalchemy import event

# Import mobile template
from flask_mobility.decorators import mobile_template

# Import the database object from the main app module
from app import db, app

# Import module forms
from app.mod_xyz.forms import XyzForm

# Import module models (e.g. User)
from app.mod_xyz.models import Xyz

# Define the blueprint: 'xyz', set its url prefix: app.url/xyz
mod_public_xyz = Blueprint('xyz_public', __name__, template_folder='templates', url_prefix='/xyz')
mod_admin_xyz = Blueprint('xyz_admin', __name__, template_folder='templates', url_prefix='/admin/xyz')


# Set the route and accepted methods
@mod_public_xyz.route('/', methods=['GET'])
@mobile_template('{mobile/}xyz/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = Xyz.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_xyz.route('/', methods=['GET'])
@mobile_template('{mobile/}xyz/admin/index.html')
@login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = Xyz.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_xyz.route('/create', methods=['GET'])
@mobile_template('{mobile/}xyz/admin/create.html')
@login_required
def create(template):

    # If in form is submitted
    form = XyzForm(request.form)

    return render_template(template, form=form)


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
@mobile_template('{mobile/}xyz/admin/show.html')
@login_required
def show(id,template):
    data = Xyz.query.get(id)

    return render_template(template, data=data)


@mod_admin_xyz.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}xyz/admin/edit.html')
@login_required
def edit(id,template):

    # If in form is submitted
    form = XyzForm(request.form)

    data = Xyz.query.get(id)

    return render_template(template, form=form, data=data)


@mod_admin_xyz.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@login_required
def update(id):
    data = Xyz.query.get(id)
    # start update request feilds
    # this line should be removed and replaced with the updateFormRequestDefinitions variable
    # end update request feilds
    # data.title = request.form.get("title")
    db.session.commit()

    return redirect(url_for('xyz_admin.index'))


@mod_admin_xyz.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Xyz.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('xyz_admin.index'))


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Xyz, "before_insert")
def before_insert(mapper, connection, target):
    pass


@event.listens_for(Xyz, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Xyz, "before_update")
def before_update(mapper, connection, target):
    pass


@event.listens_for(Xyz, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Xyz, "before_delete")
def before_delete(mapper, connection, target):
    pass


@event.listens_for(Xyz, "after_delete")
def after_delete(mapper, connection, target):
    pass
