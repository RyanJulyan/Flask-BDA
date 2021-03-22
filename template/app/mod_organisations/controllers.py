
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
from app.mod_organisations.forms import OrganisationsForm

# Import module models (e.g. User)
from app.mod_organisations.models import Organisations

# Import module models (Audit)
from app.mod_audit.models import Audit

# Define the blueprint: 'organisations', set its url prefix: app.url/organisations
mod_public_organisations = Blueprint('organisations_public', __name__, template_folder='templates', url_prefix='/organisations')
mod_admin_organisations = Blueprint('organisations_admin', __name__, template_folder='templates', url_prefix='/admin/organisations')


# Set the route and accepted methods
@mod_public_organisations.route('/', methods=['GET'])
@mobile_template('{mobile/}organisations/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = Organisations.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_organisations.route('/', methods=['GET'])
@mobile_template('{mobile/}organisations/admin/index.html')
@login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = Organisations.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_organisations.route('/create', methods=['GET'])
@mobile_template('{mobile/}organisations/admin/create.html')
@login_required
def create(template):

    # If in form is submitted
    form = OrganisationsForm(request.form)

    return render_template(template, form=form)


@mod_admin_organisations.route('/store', methods=['POST'])
@login_required
def store():
    data = Organisations(
        # start new request feilds
        organisation_name=request.form.get('organisation_name'),
        organisation_details=request.form.get('organisation_details'),
        organisation_contact_name=request.form.get('organisation_contact_name'),
        organisation_contact_email=request.form.get('organisation_contact_email'),
        organisation_address=request.form.get('organisation_address'),
        organisation_city=request.form.get('organisation_city'),
        organisation_postal_code=request.form.get('organisation_postal_code'),
        organisation_country=request.form.get('organisation_country'),
        organisation_homepage=request.form.get('organisation_homepage'),
        organisation_vat_number=request.form.get('organisation_vat_number'),
        organisation_reg_number=request.form.get('organisation_reg_number')
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

    return redirect(url_for('organisations_admin.index'))


@mod_admin_organisations.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}organisations/admin/show.html')
@login_required
def show(id,template):
    data = Organisations.query.get(id)

    return render_template(template, data=data)


@mod_admin_organisations.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}organisations/admin/edit.html')
@login_required
def edit(id,template):

    # If in form is submitted
    form = OrganisationsForm(request.form)

    data = Organisations.query.get(id)

    return render_template(template, form=form, data=data)


@mod_admin_organisations.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@login_required
def update(id):
    data = Organisations.query.get(id)
    # start update request feilds
    data.organisation_name = request.form.get('organisation_name'),
    data.organisation_details = request.form.get('organisation_details'),
    data.organisation_contact_name = request.form.get('organisation_contact_name'),
    data.organisation_contact_email = request.form.get('organisation_contact_email'),
    data.organisation_address = request.form.get('organisation_address'),
    data.organisation_city = request.form.get('organisation_city'),
    data.organisation_postal_code = request.form.get('organisation_postal_code'),
    data.organisation_country = request.form.get('organisation_country'),
    data.organisation_homepage = request.form.get('organisation_homepage'),
    data.organisation_vat_number = request.form.get('organisation_vat_number'),
    data.organisation_reg_number = request.form.get('organisation_reg_number')
    # end update request feilds
    # data.title = request.form.get("title")
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errorInfo = e.orig.args
        flash(errorInfo[0], 'error')

    return redirect(url_for('organisations_admin.index'))


@mod_admin_organisations.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Organisations.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('organisations_admin.index'))


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Organisations, "before_insert")
def before_insert(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Organisations",
        action="Before Insert",
        context="Web Form",
        payload=payload
    )
    db.session.add(data)
    pass


@event.listens_for(Organisations, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Organisations, "before_update")
def before_update(mapper, connection, target):
    pass


@event.listens_for(Organisations, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Organisations, "before_delete")
def before_delete(mapper, connection, target):
    pass


@event.listens_for(Organisations, "after_delete")
def after_delete(mapper, connection, target):
    pass
