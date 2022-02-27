
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
from app.mod_web_hooks.forms import Web_hooksForm

# Import web_hooks module models 
from app.mod_web_hooks.models import Web_hooks
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


# Define the blueprint: 'web_hooks', set its url prefix: app.url/web_hooks
mod_public_web_hooks = Blueprint('web_hooks_public', __name__, template_folder='templates', url_prefix='/web_hooks')
mod_admin_web_hooks = Blueprint('web_hooks_admin', __name__, template_folder='templates', url_prefix='/admin/web_hooks')


# Set the route and accepted methods
@mod_public_web_hooks.route('/', methods=['GET'])
@mobile_template('{mobile/}web_hooks/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = (
                Web_hooks.query
                # relationship join

                .paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])
            )

    context_data ={
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_web_hooks.route('/', methods=['GET'])
@mobile_template('{mobile/}web_hooks/admin/index.html')
# @login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = (
                Web_hooks.query
                # relationship join

                .add_columns(
                    Web_hooks.id,
                    # Web_hooks query add columns
                    Web_hooks.webhook_name.label('webhook_name'),
                                Web_hooks.run_in_module_name.label('run_in_module_name'),
                                Web_hooks.run_before_insert.label('run_before_insert'),
                                Web_hooks.run_after_insert.label('run_after_insert'),
                                Web_hooks.run_before_update.label('run_before_update'),
                                Web_hooks.run_after_update.label('run_after_update'),
                                Web_hooks.run_before_delete.label('run_before_delete'),
                                Web_hooks.run_after_delete.label('run_after_delete'),
                                Web_hooks.method.label('method'),
                                Web_hooks.data_type.label('data_type'),
                                Web_hooks.api_endpoint.label('api_endpoint'),
                                Web_hooks.api_headers.label('api_headers'),
                                Web_hooks.api_params.label('api_params'),
                                Web_hooks.active_flag.label('active_flag'),
            
                    # relationship query add columns

                )
                .paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])
            )

    context_data ={
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_web_hooks.route('/create', methods=['GET'])
@mobile_template('{mobile/}web_hooks/admin/create.html')
# @login_required
def create(template):

    form = Web_hooksForm(request.form)

    # Relationship returns

    context_data ={
        # Relationship context_data
        
    }

    return render_template(template, form=form, **context_data)


@mod_admin_web_hooks.route('/store', methods=['POST'])
@mobile_template('{mobile/}web_hooks/admin/create.html')
# @login_required
def store(template):

    form = Web_hooksForm(request.form)

    # Relationship returns

    context_data ={
        # Relationship context_data
        
    }
    
    if form.validate_on_submit():
        data = Web_hooks(
            # start new request feilds
            webhook_name=request.form.get('webhook_name'),
            run_in_module_name=request.form.get('run_in_module_name'),
            run_before_insert= True if request.form.get('run_before_insert') == 'True' else False,
            run_after_insert= True if request.form.get('run_after_insert') == 'True' else False,
            run_before_update= True if request.form.get('run_before_update') == 'True' else False,
            run_after_update= True if request.form.get('run_after_update') == 'True' else False,
            run_before_delete= True if request.form.get('run_before_delete') == 'True' else False,
            run_after_delete= True if request.form.get('run_after_delete') == 'True' else False,
            method=request.form.get('method'),
            data_type=request.form.get('data_type'),
            api_endpoint=request.form.get('api_endpoint'),
            api_headers=request.form.get('api_headers'),
            api_params=request.form.get('api_params'),
            active_flag= True if request.form.get('active_flag') == 'True' else False
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

        return redirect(url_for('web_hooks_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form, **context_data)


@mod_admin_web_hooks.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}web_hooks/admin/show.html')
# @login_required
def show(id,template):
    data = (
                Web_hooks.query
                # relationship join

                .get_or_404(id)
            )

    context_data ={
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_web_hooks.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}web_hooks/admin/edit.html')
# @login_required
def edit(id,template):

    form = Web_hooksForm(request.form)

    data = Web_hooks.query.get_or_404(id)

    web_hooks_columns = inspect(Web_hooks)

    for column in web_hooks_columns.attrs:
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


@mod_admin_web_hooks.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@mobile_template('{mobile/}web_hooks/admin/edit.html')
# @login_required
def update(id,template):

    form = Web_hooksForm(request.form)
    data = Web_hooks.query.get_or_404(id)

    # Relationship returns

    context_data ={
        "data": data,
        # Relationship context_data
        
    }
    
    if form.validate_on_submit():
        # start update request feilds
        data.webhook_name = request.form.get('webhook_name')
        data.run_in_module_name = request.form.get('run_in_module_name')
        data.run_before_insert = True if request.form.get('run_before_insert') == 'True' else False
        data.run_after_insert = True if request.form.get('run_after_insert') == 'True' else False
        data.run_before_update = True if request.form.get('run_before_update') == 'True' else False
        data.run_after_update = True if request.form.get('run_after_update') == 'True' else False
        data.run_before_delete = True if request.form.get('run_before_delete') == 'True' else False
        data.run_after_delete = True if request.form.get('run_after_delete') == 'True' else False
        data.method = request.form.get('method')
        data.data_type = request.form.get('data_type')
        data.api_endpoint = request.form.get('api_endpoint')
        data.api_headers = request.form.get('api_headers')
        data.api_params = request.form.get('api_params')
        data.active_flag =  True if request.form.get('active_flag') == 'True' else False
    # end update request feilds
        # data.title = request.form.get("title")
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            flash(errorInfo[0], 'error')

        return redirect(url_for('web_hooks_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form, **context_data)


@mod_admin_web_hooks.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
# @login_required
def destroy(id):
    data = Web_hooks.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('web_hooks_admin.index')+"?organization="+g.organization)


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Web_hooks, "before_insert")
def before_insert(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Web_hooks",
            action="Before Insert",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Web_hooks, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Web_hooks, "before_update")
def before_update(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Web_hooks",
            action="Before Update",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Web_hooks, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Web_hooks, "before_delete")
def before_delete(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Web_hooks",
            action="Before Delete",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Web_hooks, "after_delete")
def after_delete(mapper, connection, target):
    pass
