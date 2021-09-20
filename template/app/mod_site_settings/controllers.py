
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_required
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

# Import mobile template
from flask_mobility.decorators import mobile_template

# Import the database object from the main app module
from app import db, app

# Import helper functions, comment in as needed (commented out for performance)
# from app.mod_helper_functions import functions as fn

# Import module forms
from app.mod_site_settings.forms import Site_settingsForm

# Import module models (e.g. User)
from app.mod_site_settings.models import Site_settings

# Import module models (Audit)
from app.mod_audit.models import Audit
# import multiple bindings
from app.mod_tenancy.multi_bind import MultiBindSQLAlchemy
###################################################################
#### Uncomment the following enable the use different bindings ####
###################################################################

########################################################################################################################
## change db.first to db.<binding> name as needed where <binding> is the name you want to reference when making calls ##
########################################################################################################################

# db.first = MultiBindSQLAlchemy('first')
##################################################
## this will only work for the execute function ##
##################################################
# db.first.execute(...)

#########################################################################################################################
## change db.second to db.<binding> name as needed where <binding> is the name you want to reference when making calls ##
#########################################################################################################################

# db.second = MultiBindSQLAlchemy('second')
##################################################
## this will only work for the execute function ##
##################################################
# db.second.execute(...)


# Define the blueprint: 'site_settings', set its url prefix: app.url/site_settings
mod_public_site_settings = Blueprint('site_settings_public', __name__, template_folder='templates', url_prefix='/site_settings')
mod_admin_site_settings = Blueprint('site_settings_admin', __name__, template_folder='templates', url_prefix='/admin/site_settings')


# Set the route and accepted methods
@mod_public_site_settings.route('/', methods=['GET'])
@mobile_template('{mobile/}site_settings/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = Site_settings.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_site_settings.route('/', methods=['GET'])
@mobile_template('{mobile/}site_settings/admin/index.html')
@login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = Site_settings.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_site_settings.route('/create', methods=['GET'])
@mobile_template('{mobile/}site_settings/admin/create.html')
@login_required
def create(template):

    # If in form is submitted
    form = Site_settingsForm(request.form)

    return render_template(template, form=form)


@mod_admin_site_settings.route('/store', methods=['POST'])
@login_required
def store():
    data = Site_settings(
        # start new request feilds
        organisation_id=request.form.get('organisation_id'),
        key=request.form.get('key'),
        display_name=request.form.get('display_name'),
        description=request.form.get('description'),
        value=request.form.get('value'),
        data_type=request.form.get('data_type'),
        group=request.form.get('group'),
        key_value=request.form.get('key_value')
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

    return redirect(url_for('site_settings_admin.index')+"?organization="+g.organization)


@mod_admin_site_settings.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}site_settings/admin/show.html')
@login_required
def show(id,template):
    data = Site_settings.query.get(id)

    return render_template(template, data=data)


@mod_admin_site_settings.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}site_settings/admin/edit.html')
@login_required
def edit(id,template):

    # If in form is submitted
    form = Site_settingsForm(request.form)

    data = Site_settings.query.get(id)

    return render_template(template, form=form, data=data)


@mod_admin_site_settings.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@login_required
def update(id):
    data = Site_settings.query.get(id)
    # start update request feilds
    data.organisation_id = request.form.get('organisation_id')
    data.key = request.form.get('key')
    data.display_name = request.form.get('display_name')
    data.description = request.form.get('description')
    data.value = request.form.get('value')
    data.data_type = request.form.get('data_type')
    data.group = request.form.get('group')
    data.key_value = request.form.get('key_value')
    # end update request feilds
    # data.title = request.form.get("title")
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errorInfo = e.orig.args
        flash(errorInfo[0], 'error')

    return redirect(url_for('site_settings_admin.index')+"?organization="+g.organization)


@mod_admin_site_settings.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Site_settings.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('site_settings_admin.index')+"?organization="+g.organization)


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Site_settings, "before_insert")
def before_insert(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Site_settings",
        action="Before Insert",
        context="Web Form",
        payload=payload
    )
    db.session.add(data)
    db.session.commit()
    pass


@event.listens_for(Site_settings, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Site_settings, "before_update")
def before_update(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Site_settings",
        action="Before Update",
        context="Web Form",
        payload=payload
    )
    db.session.add(data)
    db.session.commit()
    pass


@event.listens_for(Site_settings, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Site_settings, "before_delete")
def before_delete(mapper, connection, target):
    pass


@event.listens_for(Site_settings, "after_delete")
def after_delete(mapper, connection, target):
    pass
