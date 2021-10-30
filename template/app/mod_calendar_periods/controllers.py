
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
from app.mod_calendar_periods.forms import Calendar_periodsForm

# Import module models (e.g. User)
from app.mod_calendar_periods.models import Calendar_periods

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


# Define the blueprint: 'calendar_periods', set its url prefix: app.url/calendar_periods
mod_public_calendar_periods = Blueprint('calendar_periods_public', __name__, template_folder='templates', url_prefix='/calendar_periods')
mod_admin_calendar_periods = Blueprint('calendar_periods_admin', __name__, template_folder='templates', url_prefix='/admin/calendar_periods')


# Set the route and accepted methods
@mod_public_calendar_periods.route('/', methods=['GET'])
@mobile_template('{mobile/}calendar_periods/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = Calendar_periods.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_calendar_periods.route('/', methods=['GET'])
@mobile_template('{mobile/}calendar_periods/admin/index.html')
@login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = Calendar_periods.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_calendar_periods.route('/create', methods=['GET'])
@mobile_template('{mobile/}calendar_periods/admin/create.html')
@login_required
def create(template):

    # If in form is submitted
    form = Calendar_periodsForm(request.form)

    return render_template(template, form=form)


@mod_admin_calendar_periods.route('/store', methods=['POST'])
@mobile_template('{mobile/}calendar_periods/admin/create.html')
@login_required
def store(template):

    form = Calendar_periodsForm(request.form)
    
    if form.validate_on_submit():
        data = Calendar_periods(
            # start new request feilds
        calendar_definition_id=request.form.get('calendar_definition_id'),
        start_date=request.form.get('start_date'),
        end_date=request.form.get('end_date'),
        day=request.form.get('day'),
        week=request.form.get('week'),
        week_day=request.form.get('week_day'),
        week_index=request.form.get('week_index'),
        month=request.form.get('month'),
        month_index=request.form.get('month_index'),
        quarter=request.form.get('quarter'),
        quarter_index=request.form.get('quarter_index'),
        year=request.form.get('year')
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

        return redirect(url_for('calendar_periods_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form)


@mod_admin_calendar_periods.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}calendar_periods/admin/show.html')
@login_required
def show(id,template):
    data = Calendar_periods.query.get(id)

    return render_template(template, data=data)


@mod_admin_calendar_periods.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}calendar_periods/admin/edit.html')
@login_required
def edit(id,template):

    # If in form is submitted
    form = Calendar_periodsForm(request.form)

    data = Calendar_periods.query.get(id)

    return render_template(template, form=form, data=data)


@mod_admin_calendar_periods.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@mobile_template('{mobile/}calendar_periods/admin/edit.html')
@login_required
def update(id,template):

    form = Calendar_periodsForm(request.form)
    
    if form.validate_on_submit():
        data = Calendar_periods.query.get(id)
        # start update request feilds
        data.calendar_definition_id = request.form.get('calendar_definition_id')
        data.start_date = request.form.get('start_date')
        data.end_date = request.form.get('end_date')
        data.day = request.form.get('day')
        data.week = request.form.get('week')
        data.week_day = request.form.get('week_day')
        data.week_index = request.form.get('week_index')
        data.month = request.form.get('month')
        data.month_index = request.form.get('month_index')
        data.quarter = request.form.get('quarter')
        data.quarter_index = request.form.get('quarter_index')
        data.year = request.form.get('year')
    # end update request feilds
        # data.title = request.form.get("title")
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            flash(errorInfo[0], 'error')

        return redirect(url_for('calendar_periods_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form)


@mod_admin_calendar_periods.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Calendar_periods.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('calendar_periods_admin.index')+"?organization="+g.organization)


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Calendar_periods, "before_insert")
def before_insert(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_periods",
            action="Before Insert",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_periods, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Calendar_periods, "before_update")
def before_update(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_periods",
            action="Before Update",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_periods, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Calendar_periods, "before_delete")
def before_delete(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_periods",
            action="Before Delete",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_periods, "after_delete")
def after_delete(mapper, connection, target):
    pass
