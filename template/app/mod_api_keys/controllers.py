
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
from app.mod_api_keys.forms import Api_keysForm

# Import module models (e.g. User)
from app.mod_api_keys.models import Api_keys

# Import module models (Audit)
from app.mod_audit.models import Audit

# Define the blueprint: 'api_keys', set its url prefix: app.url/api_keys
mod_public_api_keys = Blueprint('api_keys_public', __name__, template_folder='templates', url_prefix='/api_keys')
mod_admin_api_keys = Blueprint('api_keys_admin', __name__, template_folder='templates', url_prefix='/admin/api_keys')


# Set the route and accepted methods
@mod_public_api_keys.route('/', methods=['GET'])
@mobile_template('{mobile/}api_keys/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = Api_keys.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_api_keys.route('/', methods=['GET'])
@mobile_template('{mobile/}api_keys/admin/index.html')
@login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = Api_keys.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_api_keys.route('/create', methods=['GET'])
@mobile_template('{mobile/}api_keys/admin/create.html')
@login_required
def create(template):

    # If in form is submitted
    form = Api_keysForm(request.form)

    return render_template(template, form=form)


@mod_admin_api_keys.route('/store', methods=['POST'])
@login_required
def store():
    data = Api_keys(
        # start new request feilds
        api_key=request.form.get('api_key'),
        api_key_notes=request.form.get('api_key_notes'),
        created_user_id=request.form.get('created_user_id'),
        valid_from=request.form.get('valid_from'),
        valid_to=request.form.get('valid_to')
        # end new request feilds
        # title=request.form.get("title")
    )
    db.session.add(data)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errorInfo = e.orig.args
        flash(errorInfo[0], 'error')

    return redirect(url_for('api_keys_admin.index'))


@mod_admin_api_keys.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}api_keys/admin/show.html')
@login_required
def show(id,template):
    data = Api_keys.query.get(id)

    return render_template(template, data=data)


@mod_admin_api_keys.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}api_keys/admin/edit.html')
@login_required
def edit(id,template):

    # If in form is submitted
    form = Api_keysForm(request.form)

    data = Api_keys.query.get(id)

    return render_template(template, form=form, data=data)


@mod_admin_api_keys.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@login_required
def update(id):
    data = Api_keys.query.get(id)
    # start update request feilds
    data.api_key = request.form.get('api_key'),
    data.api_key_notes = request.form.get('api_key_notes'),
    data.created_user_id = request.form.get('created_user_id'),
    data.valid_from = request.form.get('valid_from'),
    data.valid_to = request.form.get('valid_to')
    # end update request feilds
    # data.title = request.form.get("title")
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errorInfo = e.orig.args
        flash(errorInfo[0], 'error')

    return redirect(url_for('api_keys_admin.index'))


@mod_admin_api_keys.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Api_keys.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('api_keys_admin.index'))


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Api_keys, "before_insert")
def before_insert(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Api_keys",
        action="Before Insert",
        context="Web Form",
        payload=payload
    )
    db.session.add(data)
    pass


@event.listens_for(Api_keys, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Api_keys, "before_update")
def before_update(mapper, connection, target):
    pass


@event.listens_for(Api_keys, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Api_keys, "before_delete")
def before_delete(mapper, connection, target):
    pass


@event.listens_for(Api_keys, "after_delete")
def after_delete(mapper, connection, target):
    pass
