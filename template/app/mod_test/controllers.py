
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
from app.mod_test.forms import TestForm

# Import module models (e.g. User)
from app.mod_test.models import Test

# Import module models (Audit)
from app.mod_audit.models import Audit

# Define the blueprint: 'test', set its url prefix: app.url/test
mod_public_test = Blueprint('test_public', __name__, template_folder='templates', url_prefix='/test')
mod_admin_test = Blueprint('test_admin', __name__, template_folder='templates', url_prefix='/admin/test')


# Set the route and accepted methods
@mod_public_test.route('/', methods=['GET'])
@mobile_template('{mobile/}test/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = Test.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_test.route('/', methods=['GET'])
@mobile_template('{mobile/}test/admin/index.html')
@login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = Test.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_test.route('/create', methods=['GET'])
@mobile_template('{mobile/}test/admin/create.html')
@login_required
def create(template):

    # If in form is submitted
    form = TestForm(request.form)

    return render_template(template, form=form)


@mod_admin_test.route('/store', methods=['POST'])
@login_required
def store():
    data = Test(
        # start new request feilds
        name=request.form.get('name')
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

    return redirect(url_for('test_admin.index'))


@mod_admin_test.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}test/admin/show.html')
@login_required
def show(id,template):
    data = Test.query.get(id)

    return render_template(template, data=data)


@mod_admin_test.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}test/admin/edit.html')
@login_required
def edit(id,template):

    # If in form is submitted
    form = TestForm(request.form)

    data = Test.query.get(id)

    return render_template(template, form=form, data=data)


@mod_admin_test.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@login_required
def update(id):
    data = Test.query.get(id)
    # start update request feilds
    data.name = request.form.get('name')
    # end update request feilds
    # data.title = request.form.get("title")
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errorInfo = e.orig.args
        flash(errorInfo[0], 'error')

    return redirect(url_for('test_admin.index'))


@mod_admin_test.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Test.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('test_admin.index'))


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Test, "before_insert")
def before_insert(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Test",
        action="Before Insert",
        context="Web Form",
        payload=payload
    )
    db.session.add(data)
    pass


@event.listens_for(Test, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Test, "before_update")
def before_update(mapper, connection, target):
    pass


@event.listens_for(Test, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Test, "before_delete")
def before_delete(mapper, connection, target):
    pass


@event.listens_for(Test, "after_delete")
def after_delete(mapper, connection, target):
    pass
