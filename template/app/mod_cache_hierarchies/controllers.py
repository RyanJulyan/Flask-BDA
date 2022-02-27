
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_required
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

import math

# Import mobile template
from flask_mobility.decorators import mobile_template

# Import the database object from the main app module
from app import db, app
# Import sql functions (SUM,MIN,MAX,AVG)
from sqlalchemy.sql import func

# Import helper functions, comment in as needed (commented out for performance)
# from app.mod_helper_functions import functions as fn

# Import module forms
from app.mod_cache_hierarchies.forms import Cache_hierarchiesForm

# Import module models (e.g. User)
from app.mod_cache_hierarchies.models import Cache_hierarchies
from app.mod_hierarchies.models import Hierarchies

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


# Define the blueprint: 'cache_hierarchies', set its url prefix: app.url/cache_hierarchies
mod_public_cache_hierarchies = Blueprint('cache_hierarchies_public', __name__, template_folder='templates', url_prefix='/cache_hierarchies')
mod_admin_cache_hierarchies = Blueprint('cache_hierarchies_admin', __name__, template_folder='templates', url_prefix='/admin/cache_hierarchies')


# Set the route and accepted methods
@mod_public_cache_hierarchies.route('/', methods=['GET'])
@mobile_template('{mobile/}cache_hierarchies/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = Cache_hierarchies.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_cache_hierarchies.route('/', methods=['GET'])
@mobile_template('{mobile/}cache_hierarchies/admin/index.html')
@login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = Cache_hierarchies.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_cache_hierarchies.route('/create', methods=['GET'])
@mobile_template('{mobile/}cache_hierarchies/admin/create.html')
@login_required
def create(template):

    hierarchy_count = Hierarchies.query.count()
    level_max = Hierarchies.query.with_entities(
                                        func.max(Hierarchies.level).label('level_max')).one()
    max_hierarchy_cache_count = 0
    for i in range(0,level_max[0]+1):
        max_hierarchy_cache_count += i

    # If in form is submitted
    form = Cache_hierarchiesForm(request.form)

    return render_template(template, form=form, hierarchy_count=hierarchy_count, max_hierarchy_cache_count=max_hierarchy_cache_count)


@mod_admin_cache_hierarchies.route('/store', methods=['POST'])
@login_required
def store():

    num_rows_deleted = Cache_hierarchies.query.delete()
    db.session.commit()

    hierarchies = Hierarchies.query.all()

    for hierarchy in hierarchies:
        organisation_id = hierarchy.organisation_id
        hierarchy_id = hierarchy.id
        name = hierarchy.name
        path = hierarchy.path
        level = hierarchy.level
        parent_id = hierarchy.parent_id
        key_value = hierarchy.key_value

        current_hierarchy_ids = path.split('/')
        current_hierarchy_ids = current_hierarchy_ids[:] = [int(x) for x in current_hierarchy_ids if x]

        for current_hierarchy_id in current_hierarchy_ids:
            data = Cache_hierarchies(
                # start new request feilds
                organisation_id=organisation_id,
                current_hierarchy_id=current_hierarchy_id,
                hierarchy_id=hierarchy_id,
                name=name,
                path=path,
                level=level,
                parent_id=parent_id,
                key_value=key_value
                # end new request feilds
                # title=request.form.get("title")
            )
            db.session.add(data)
        
        hierarchy.cached = bool(1)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errorInfo = e.orig.args
        flash(errorInfo[0], 'error')

    return redirect(url_for('cache_hierarchies_admin.index')+"?organization="+g.organization)


@mod_admin_cache_hierarchies.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}cache_hierarchies/admin/show.html')
@login_required
def show(id,template):
    data = Cache_hierarchies.query.get(id)

    return render_template(template, data=data)


@mod_admin_cache_hierarchies.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}cache_hierarchies/admin/edit.html')
@login_required
def edit(id,template):

    # If in form is submitted
    form = Cache_hierarchiesForm(request.form)

    data = Cache_hierarchies.query.get(id)

    return render_template(template, form=form, data=data)


@mod_admin_cache_hierarchies.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
@login_required
def update(id):
    data = Cache_hierarchies.query.get(id)
    # start update request feilds
    data.organisation_id = request.form.get('organisation_id')
    data.current_hierarchy_id = request.form.get('current_hierarchy_id')
    data.hierarchy_id = request.form.get('hierarchy_id')
    data.name = request.form.get('name')
    data.path = request.form.get('path')
    data.level = request.form.get('level')
    data.parent_id = request.form.get('parent_id')
    data.key_value = request.form.get('key_value')
    # end update request feilds
    # data.title = request.form.get("title")
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errorInfo = e.orig.args
        flash(errorInfo[0], 'error')

    return redirect(url_for('cache_hierarchies_admin.index')+"?organization="+g.organization)


@mod_admin_cache_hierarchies.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def destroy(id):
    data = Cache_hierarchies.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('cache_hierarchies_admin.index')+"?organization="+g.organization)


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Cache_hierarchies, "before_insert")
def before_insert(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Cache_hierarchies",
        action="Before Insert",
        context="Web Form",
        payload=payload
    )
    db.session.add(data)
    pass


@event.listens_for(Cache_hierarchies, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Cache_hierarchies, "before_update")
def before_update(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Cache_hierarchies",
        action="Before Update",
        context="Web Form",
        payload=payload
    )
    db.session.add(data)
    pass


@event.listens_for(Cache_hierarchies, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Cache_hierarchies, "before_delete")
def before_delete(mapper, connection, target):
    pass


@event.listens_for(Cache_hierarchies, "after_delete")
def after_delete(mapper, connection, target):
    pass
