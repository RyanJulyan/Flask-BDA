
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_required
from sqlalchemy import event, inspect, and_, or_
from sqlalchemy.exc import IntegrityError

# Import mobile template
from flask_mobility.decorators import mobile_template

# Import the database object from the main app module
from app import db, app

# Import helper functions, comment in as needed (commented out for performance)
from app.mod_helper_functions import functions as fn

# Import module forms
from app.mod_statuses.forms import StatusesForm

# Import statuses module models 
from app.mod_statuses.models import Statuses
# Import module models (e.g. User)


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


# Define the blueprint: 'statuses', set its url prefix: app.url/statuses
mod_public_statuses = Blueprint('statuses_public', __name__, template_folder='templates', url_prefix='/statuses')
mod_admin_statuses = Blueprint('statuses_admin', __name__, template_folder='templates', url_prefix='/admin/statuses')


# Set the route and accepted methods
@mod_public_statuses.route('/', methods=['GET'])
@mobile_template('{mobile/}statuses/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = (
                Statuses.query
                # relationship join

                .paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])
            )

    context_data ={
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_statuses.route('/', methods=['GET'])
@mobile_template('{mobile/}statuses/admin/index.html')
@login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = (
                Statuses.query
                # relationship join

                .add_columns(
                    Statuses.id,
                    # Statuses query add columns
                    Statuses.status_key.label('status_key'),
                                Statuses.status_display_name.label('status_display_name'),
                                Statuses.status_description.label('status_description'),
                                Statuses.status_group.label('status_group'),
                                Statuses.key_value.label('key_value'),
            
                    # relationship query add columns

                )
                .paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])
            )

    context_data ={
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_statuses.route('/create', methods=['GET'])
@mobile_template('{mobile/}statuses/admin/create.html')
@login_required
def create(template):

    form = StatusesForm(request.form)

    # Relationship returns

    context_data ={
        # Relationship context_data
        
    }

    return render_template(template, form=form, **context_data)


@mod_admin_statuses.route('/store', methods=['POST'])
@mobile_template('{mobile/}statuses/admin/create.html')
@login_required
def store(template):

    form = StatusesForm(request.form)

    # Relationship returns

    context_data ={
        # Relationship context_data
        
    }
    
    if form.validate_on_submit():
        data = Statuses(
            # start new request feilds
            status_key=request.form.get('status_key'),
            status_display_name=request.form.get('status_display_name'),
            status_description=request.form.get('status_description'),
            status_group=request.form.get('status_group'),
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

        return redirect(url_for('statuses_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form, **context_data)


@mod_admin_statuses.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}statuses/admin/show.html')
@login_required
def show(id,template):
    data = (
                Statuses.query
                # relationship join

                .get_or_404(id)
            )

    context_data ={
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_statuses.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}statuses/admin/edit.html')
@login_required
def edit(id,template):

    form = StatusesForm(request.form)

    data = Statuses.query.get_or_404(id)

    statuses_columns = inspect(Statuses)

    for column in statuses_columns.attrs:
        column_name = column.key
        try:
            form[column_name].data = getattr(data,column_name)
        except:
            pass

    # Relationship returns

    context_data ={
        "data": data,
        # Relationship context_data
        
    }

    return render_template(template, form=form, **context_data)


@mod_admin_statuses.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@mobile_template('{mobile/}statuses/admin/edit.html')
@login_required
def update(id,template):

    form = StatusesForm(request.form)
    data = Statuses.query.get_or_404(id)

    # Relationship returns

    context_data ={
        "data": data,
        # Relationship context_data
        
    }
    
    if form.validate_on_submit():
        # start update request feilds
        data.status_key = request.form.get('status_key')
        data.status_display_name = request.form.get('status_display_name')
        data.status_description = request.form.get('status_description')
        data.status_group = request.form.get('status_group')
        data.key_value = request.form.get('key_value')
    # end update request feilds
        # data.title = request.form.get("title")
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            flash(errorInfo[0], 'error')

        return redirect(url_for('statuses_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form, **context_data)


@mod_admin_statuses.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Statuses.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('statuses_admin.index')+"?organization="+g.organization)


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Statuses, "before_insert")
def before_insert(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Statuses",
            action="Before Insert",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'statuses', run_type = "before_insert", data = data, convert_sqlalchemy_to_json = True)

    pass


@event.listens_for(Statuses, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Statuses, "before_update")
def before_update(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Statuses",
            action="Before Update",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'statuses', run_type = "before_insert", data = data, convert_sqlalchemy_to_json = True)
    pass


@event.listens_for(Statuses, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Statuses, "before_delete")
def before_delete(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Statuses",
            action="Before Delete",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'statuses', run_type = "before_insert", data = data, convert_sqlalchemy_to_json = True)
    pass


@event.listens_for(Statuses, "after_delete")
def after_delete(mapper, connection, target):
    pass
