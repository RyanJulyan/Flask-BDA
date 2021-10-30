
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
from app.mod_test.forms import TestForm

# Import test module models 
from app.mod_test.models import Test
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


# Define the blueprint: 'test', set its url prefix: app.url/test
mod_public_test = Blueprint('test_public', __name__, template_folder='templates', url_prefix='/test')
mod_admin_test = Blueprint('test_admin', __name__, template_folder='templates', url_prefix='/admin/test')


# Set the route and accepted methods
@mod_public_test.route('/', methods=['GET'])
@mobile_template('{mobile/}test/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = (
                Test.query
                # relationship join
                .join(Users)
                .paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])
            )

    context_data ={
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_test.route('/', methods=['GET'])
@mobile_template('{mobile/}test/admin/index.html')
@login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = (
                Test.query
                # relationship join
                .join(Users)
                .add_columns(
                    Test.id,
                    # Test query add columns
                    Test.budget.label('budget'),
                                Test.name.label('name'),
                                Test.start_date.label('start_date'),
                                Test.end_datetime.label('end_datetime'),
            
                    # relationship query add columns
                    Users.name.label('users_name'),
            
                )
                .paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])
            )

    context_data ={
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_test.route('/create', methods=['GET'])
@mobile_template('{mobile/}test/admin/create.html')
@login_required
def create(template):

    form = TestForm(request.form)

    # Relationship returns
    users = Users.query.all()
    context_data ={
        # Relationship context_data

        'users': users        
    }

    return render_template(template, form=form, **context_data)


@mod_admin_test.route('/store', methods=['POST'])
@mobile_template('{mobile/}test/admin/create.html')
@login_required
def store(template):

    form = TestForm(request.form)

    # Relationship returns
    users = Users.query.all()
    context_data ={
        # Relationship context_data

        'users': users        
    }
    
    if form.validate_on_submit():
        data = Test(
            # start new request feilds
            budget=request.form.get('budget'),
            name=request.form.get('name'),
            start_date=fn.convert_to_python_data_type('date')(request.form.get('start_date')),
            end_datetime=fn.convert_to_python_data_type('datetime')(request.form.get('end_datetime')),
            test_id=request.form.get('test_id')
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

        return redirect(url_for('test_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form, **context_data)


@mod_admin_test.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}test/admin/show.html')
@login_required
def show(id,template):
    data = (
                Test.query
                # relationship join
                .join(Users)
                .get_or_404(id)
            )

    context_data ={
        "data": data,
    }

    return render_template(template, **context_data)


@mod_admin_test.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}test/admin/edit.html')
@login_required
def edit(id,template):

    form = TestForm(request.form)

    data = Test.query.get_or_404(id)

    test_columns = inspect(Test)

    for column in test_columns.attrs:
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


@mod_admin_test.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@mobile_template('{mobile/}test/admin/edit.html')
@login_required
def update(id,template):

    form = TestForm(request.form)
    data = Test.query.get_or_404(id)

    # Relationship returns
    users = Users.query.all()
    context_data ={
        "data": data,
        # Relationship context_data

        'users': users        
    }
    
    if form.validate_on_submit():
        # start update request feilds
        data.budget = request.form.get('budget')
        data.name = request.form.get('name')
        data.start_date = fn.convert_to_python_data_type('date')(request.form.get('start_date'))
        data.end_datetime = fn.convert_to_python_data_type('datetime')(request.form.get('end_datetime'))
        data.test_id = request.form.get('test_id')
    # end update request feilds
        # data.title = request.form.get("title")
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            flash(errorInfo[0], 'error')

        return redirect(url_for('test_admin.index')+"?organization="+g.organization)
    else:
        return render_template(template, form=form, **context_data)


@mod_admin_test.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Test.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('test_admin.index')+"?organization="+g.organization)


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Test, "before_insert")
def before_insert(mapper, connection, target):
    if request.form:
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
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Test",
            action="Before Update",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Test, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Test, "before_delete")
def before_delete(mapper, connection, target):
    if request.form:
        payload = '{'
        for obj in request.form:
            payload += '"' + obj + '": "' + request.form.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Test",
            action="Before Delete",
            context="Web Form",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Test, "after_delete")
def after_delete(mapper, connection, target):
    pass
