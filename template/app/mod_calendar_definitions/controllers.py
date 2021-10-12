
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_required
from sqlalchemy import event, and_, or_
from sqlalchemy.exc import IntegrityError

# Import mobile template
from flask_mobility.decorators import mobile_template

# Import the database object from the main app module
from app import db, app

# Import helper functions, comment in as needed (commented out for performance)
# from app.mod_helper_functions import functions as fn

# Import module forms
from app.mod_calendar_definitions.forms import Calendar_definitionsForm

# Import module models (e.g. User)
from app.mod_calendar_definitions.models import Calendar_definitions

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


# Define the blueprint: 'calendar_definitions', set its url prefix: app.url/calendar_definitions
mod_public_calendar_definitions = Blueprint('calendar_definitions_public', __name__, template_folder='templates', url_prefix='/calendar_definitions')
mod_admin_calendar_definitions = Blueprint('calendar_definitions_admin', __name__, template_folder='templates', url_prefix='/admin/calendar_definitions')


# Set the route and accepted methods
@mod_public_calendar_definitions.route('/', methods=['GET'])
@mobile_template('{mobile/}calendar_definitions/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = Calendar_definitions.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_calendar_definitions.route('/', methods=['GET'])
@mobile_template('{mobile/}calendar_definitions/admin/index.html')
@login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = Calendar_definitions.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_calendar_definitions.route('/create', methods=['GET'])
@mobile_template('{mobile/}calendar_definitions/admin/create.html')
@login_required
def create(template):

    # If in form is submitted
    form = Calendar_definitionsForm(request.form)

    return render_template(template, form=form)


@mod_admin_calendar_definitions.route('/store', methods=['POST'])
@mobile_template('{mobile/}calendar_definitions/admin/create.html')
@login_required
def store(template):

    form = Calendar_definitionsForm(request.form)
    
    if form.validate_on_submit():
        data = Calendar_definitions(
            # start new request feilds
        name=request.form.get('name'),
        start=request.form.get('start'),
        end=request.form.get('end'),
        range_history_periods=request.form.get('range_history_periods'),
        range_future_periods=request.form.get('range_future_periods'),
        freq_period_start_day=request.form.get('freq_period_start_day'),
        freq_normalize=request.form.get('freq_normalize'),
        freq_closed=request.form.get('freq_closed')
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

        return redirect(url_for('calendar_definitions_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form)


@mod_admin_calendar_definitions.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}calendar_definitions/admin/show.html')
@login_required
def show(id,template):
    data = Calendar_definitions.query.get(id)

    return render_template(template, data=data)


@mod_admin_calendar_definitions.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}calendar_definitions/admin/edit.html')
@login_required
def edit(id,template):

    # If in form is submitted
    form = Calendar_definitionsForm(request.form)

    data = Calendar_definitions.query.get(id)

    return render_template(template, form=form, data=data)


@mod_admin_calendar_definitions.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@mobile_template('{mobile/}calendar_definitions/admin/edit.html')
@login_required
def update(id,template):

    form = Calendar_definitionsForm(request.form)
    
    if form.validate_on_submit():
        data = Calendar_definitions.query.get(id)
        # start update request feilds
        data.name = request.form.get('name')
        data.start = request.form.get('start')
        data.end = request.form.get('end')
        data.range_history_periods = request.form.get('range_history_periods')
        data.range_future_periods = request.form.get('range_future_periods')
        data.freq_period_start_day = request.form.get('freq_period_start_day')
        data.freq_normalize = request.form.get('freq_normalize')
        data.freq_closed = request.form.get('freq_closed')
    # end update request feilds
        # data.title = request.form.get("title")
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            flash(errorInfo[0], 'error')

        return redirect(url_for('calendar_definitions_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form)


@mod_admin_calendar_definitions.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Calendar_definitions.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('calendar_definitions_admin.index')+"?organization="+g.organization)


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Calendar_definitions, "before_insert")
def before_insert(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_definitions",
            action="Before Insert",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_definitions, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Calendar_definitions, "before_update")
def before_update(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_definitions",
            action="Before Update",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_definitions, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Calendar_definitions, "before_delete")
def before_delete(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_definitions",
            action="Before Delete",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_definitions, "after_delete")
def after_delete(mapper, connection, target):
    pass
