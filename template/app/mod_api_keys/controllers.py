
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_required
from sqlalchemy import event, inspect, and_, or_
from sqlalchemy.exc import IntegrityError

#Import json
import json

# Import mobile template
from flask_mobility.decorators import mobile_template

# Import the database object from the main app module
from app import db, app

# Import helper functions, comment in as needed (commented out for performance)
from app.mod_helper_functions import functions as fn

# Import module forms
from app.mod_api_keys.forms import Api_keysForm

# Import api_keys module models 
from app.mod_api_keys.models import Api_keys
# Import module models (e.g. User)
from app.mod_users.models import Users

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


# Define the blueprint: 'api_keys', set its url prefix: app.url/api_keys
mod_public_api_keys = Blueprint('api_keys_public', __name__, template_folder='templates', url_prefix='/api_keys')
mod_admin_api_keys = Blueprint('api_keys_admin', __name__, template_folder='templates', url_prefix='/admin/api_keys')


# Set the route and accepted methods
@mod_public_api_keys.route('/', methods=['GET'])
@mobile_template('{mobile/}api_keys/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = (
                Api_keys.query
                # relationship join
                .join(Users)
                .paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])
            )

    context_data ={
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_api_keys.route('/', methods=['GET'])
@mobile_template('{mobile/}api_keys/admin/index.html')
@login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = (
                Api_keys.query
                # relationship join
                .join(Users)
                .add_columns(
                    Api_keys.id,
                    # Api_keys query add columns
                    Api_keys.api_key.label('api_key'),
                                Api_keys.api_key_notes.label('api_key_notes'),
                                Api_keys.valid_from.label('valid_from'),
                                Api_keys.valid_to.label('valid_to'),
            
                    # relationship query add columns
                    Users.name.label('users_name'),
            
                )
                .paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])
            )

    context_data = {
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_api_keys.route('/create', methods=['GET'])
@mobile_template('{mobile/}api_keys/admin/create.html')
@login_required
def create(template):

    form = Api_keysForm(request.form)

    # Relationship returns
    users = Users.query.all()
    context_data = {
        # Relationship context_data

        'users': users        
    }

    return render_template(template, form=form, **context_data)


@mod_admin_api_keys.route('/store', methods=['POST'])
@mobile_template('{mobile/}api_keys/admin/create.html')
@login_required
def store(template):

    form = Api_keysForm(request.form)

    # Relationship returns
    users = Users.query.all()
    context_data ={
        # Relationship context_data

        'users': users        
    }
    
    if form.validate_on_submit():
        data = Api_keys(
            # start new request feilds
            api_key = request.form.get('api_key'),
            api_key_notes = request.form.get('api_key_notes'),
            created_user_id = request.form.get('created_user_id'),
            valid_from = fn.convert_to_python_data_type('datetime')(request.form.get('valid_from')),
            valid_to = fn.convert_to_python_data_type('datetime')(request.form.get('valid_to'))
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

        return redirect(url_for('api_keys_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form, **context_data)


@mod_admin_api_keys.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}api_keys/admin/show.html')
@login_required
def show(id,template):
    data = (
                Api_keys.query
                # relationship join
                .join(Users)
                .get_or_404(id)
            )

    context_data ={
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_api_keys.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}api_keys/admin/edit.html')
@login_required
def edit(id,template):

    form = Api_keysForm(request.form)

    data = Api_keys.query.get_or_404(id)

    api_keys_columns = inspect(Api_keys)

    for column in api_keys_columns.attrs:
        column_name = column.key
        try:
            form[column_name].data = getattr(data,column_name)
        except:
            pass

    # Relationship returns
    users = Users.query.all()
    context_data ={
        "data": data,
        # Relationship context_data

        'users': users        
    }

    return render_template(template, form=form, **context_data)


@mod_admin_api_keys.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@mobile_template('{mobile/}api_keys/admin/edit.html')
@login_required
def update(id,template):

    form = Api_keysForm(request.form)
    data = Api_keys.query.get_or_404(id)

    # Relationship returns
    users = Users.query.all()
    context_data ={
        "data": data,
        # Relationship context_data

        'users': users        
    }
    
    if form.validate_on_submit():
        # start update request feilds
        data.api_key = request.form.get('api_key')
        data.api_key_notes = request.form.get('api_key_notes')
        data.created_user_id = request.form.get('created_user_id')
        data.valid_from = fn.convert_to_python_data_type('datetime')(request.form.get('valid_from'))
        data.valid_to = fn.convert_to_python_data_type('datetime')(request.form.get('valid_to'))
    # end update request feilds
        # data.title = request.form.get("title")
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            flash(errorInfo[0], 'error')

        return redirect(url_for('api_keys_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form, **context_data)


@mod_admin_api_keys.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Api_keys.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('api_keys_admin.index')+"?organization="+g.organization)


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Api_keys, "before_insert")
def before_insert(mapper, connection, target):
    if request.form:
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

        fn.process_webhook(module_name = 'api_keys', run_type = "before_insert", data = payload, convert_sqlalchemy_to_json = False)

    pass


@event.listens_for(Api_keys, "after_insert")
def after_insert(mapper, connection, target):
    if request.form:
        payload =str(json.dumps(target.as_dict(), indent=4, default=str))
        
        data = Audit(
            model_name="Api_keys",
            action="After Insert",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'api_keys', run_type = "after_insert", data = payload, convert_sqlalchemy_to_json = False)
    pass


@event.listens_for(Api_keys, "before_update")
def before_update(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Api_keys",
            action="Before Update",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'api_keys', run_type = "before_insert", data = payload, convert_sqlalchemy_to_json = False)
    pass


@event.listens_for(Api_keys, "after_update")
def after_update(mapper, connection, target):
    if request.form:
        payload =str(json.dumps(target.as_dict(), indent=4, default=str))
        
        data = Audit(
            model_name="Api_keys",
            action="After Update",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'api_keys', run_type = "after_update", data = payload, convert_sqlalchemy_to_json = False)
    pass


@event.listens_for(Api_keys, "before_delete")
def before_delete(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Api_keys",
            action="Before Delete",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'api_keys', run_type = "before_delete", data = payload, convert_sqlalchemy_to_json = False)
    pass


@event.listens_for(Api_keys, "after_delete")
def after_delete(mapper, connection, target):
    pass
