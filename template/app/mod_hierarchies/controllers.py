
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_required
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

# Import mobile template
from flask_mobility.decorators import mobile_template

# Import the database object from the main app module
from app import db, app

# Import module forms
from app.mod_hierarchies.forms import HierarchiesForm

# Import module models (e.g. User)
from app.mod_hierarchies.models import Hierarchies

# Import module models (Audit)
from app.mod_audit.models import Audit

# Define the blueprint: 'hierarchies', set its url prefix: app.url/hierarchies
mod_public_hierarchies = Blueprint('hierarchies_public', __name__, template_folder='templates', url_prefix='/hierarchies')
mod_admin_hierarchies = Blueprint('hierarchies_admin', __name__, template_folder='templates', url_prefix='/admin/hierarchies')


# Set the route and accepted methods
@mod_public_hierarchies.route('/', methods=['GET'])
@mobile_template('{mobile/}hierarchies/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = Hierarchies.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_hierarchies.route('/', methods=['GET'])
@mobile_template('{mobile/}hierarchies/admin/index.html')
# @login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = Hierarchies.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_hierarchies.route('/create', methods=['GET'])
@mobile_template('{mobile/}hierarchies/admin/create.html')
# @login_required
def create(template):

    # If in form is submitted
    form = HierarchiesForm(request.form)

    return render_template(template, form=form)


@mod_admin_hierarchies.route('/store', methods=['POST'])
# @login_required
def store():

    delim = '/'

    parent_id = request.form.get('parent_id')

    if not parent_id:
        parent_id = 1

    parent = Hierarchies.query.get(parent_id)

    if parent:
        rank = parent.path.count(delim)
        path = parent.path
    else:
        rank = 1
        path = '/1/'
    
    data = Hierarchies(
        # start new request feilds
        organisation_id = request.form.get('organisation_id'),
        name = request.form.get('name'),
        path = path,
        rank = rank,
        parent_id = parent_id,
        key_value = request.form.get('key_value')
        # end new request feilds
        # title=request.form.get("title")
    )
    db.session.add(data)
    curr_id = data.inserted_primary_key
    
    data.path = data.path + curr_id + delim

    data.rank = data.path.count(delim)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errorInfo = e.orig.args
        flash(errorInfo[0], 'error')

    return redirect(url_for('hierarchies_admin.index'))


@mod_admin_hierarchies.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}hierarchies/admin/show.html')
@login_required
def show(id,template):
    data = Hierarchies.query.get(id)

    return render_template(template, data=data)


@mod_admin_hierarchies.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}hierarchies/admin/edit.html')
@login_required
def edit(id,template):

    # If in form is submitted
    form = HierarchiesForm(request.form)

    data = Hierarchies.query.get(id)

    return render_template(template, form=form, data=data)


@mod_admin_hierarchies.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@login_required
def update(id):
    data = Hierarchies.query.get(id)
    # start update request feilds
    data.organisation_id = request.form.get('organisation_id'),
    data.name = request.form.get('name'),
    data.path = request.form.get('path'),
    data.rank = request.form.get('rank'),
    data.parent_id = request.form.get('parent_id'),
    data.key_value = request.form.get('key_value')
    # end update request feilds
    # data.title = request.form.get("title")
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errorInfo = e.orig.args
        flash(errorInfo[0], 'error')

    return redirect(url_for('hierarchies_admin.index'))


@mod_admin_hierarchies.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Hierarchies.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('hierarchies_admin.index'))


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Hierarchies, "before_insert")
def before_insert(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Hierarchies",
        action="Before Insert",
        context="Web Form",
        payload=payload
    )
    db.session.add(data)
    pass


@event.listens_for(Hierarchies, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Hierarchies, "before_update")
def before_update(mapper, connection, target):
    pass


@event.listens_for(Hierarchies, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Hierarchies, "before_delete")
def before_delete(mapper, connection, target):
    pass


@event.listens_for(Hierarchies, "after_delete")
def after_delete(mapper, connection, target):
    pass
