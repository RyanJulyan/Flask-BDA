
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_required
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

# Import mobile template
from flask_mobility.decorators import mobile_template

# Import the database object from the main app module
from app import db, app

# Import helper functions
from app.mod_helper_functions import functions as fn

# Import module forms
from app.mod_hierarchies.forms import HierarchiesForm

# Import module models (e.g. User)
from app.mod_hierarchies.models import Hierarchies
from app.mod_cache_hierarchies.models import Cache_hierarchies

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


# Define the blueprint: 'hierarchies', set its url prefix: app.url/hierarchies
mod_public_hierarchies = Blueprint('hierarchies_public', __name__, template_folder='templates', url_prefix='/hierarchies')
mod_admin_hierarchies = Blueprint('hierarchies_admin', __name__, template_folder='templates', url_prefix='/admin/hierarchies')


# Set the route and accepted methods
@mod_public_hierarchies.route('/', methods=['GET'])
@mobile_template('{mobile/}hierarchies/public/public_list.html')
def public_list(template):
    page = request.args.get('page', 1, type=int)
    data = Hierarchies.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_hierarchies.route('/', methods=['GET'])
@mobile_template('{mobile/}hierarchies/admin/index.html')
# @login_required
def index(template):
    page = request.args.get('page', 1, type=int)
    data = Hierarchies.query.order_by(Hierarchies.path).paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

    return render_template(template, data=data)


@mod_admin_hierarchies.route('/create', methods=['GET'])
@mobile_template('{mobile/}hierarchies/admin/create.html')
# @login_required
def create(template):

    parents = Hierarchies.query.all()

    # If in form is submitted
    form = HierarchiesForm(request.form)

    return render_template(template, form=form, parents=parents)


@mod_admin_hierarchies.route('/store', methods=['POST'])
# @login_required
def store():

    delimiter = '/'

    organisation_id=request.form.get('organisation_id')
    name=request.form.get('name')
    level=1
    key_value=request.form.get('key_value')

    parent_id=request.form.get('parent_id')
    if parent_id is None or parent_id == '':
        parent_id = 1

    parent_hierarchy = Hierarchies.query.get(parent_id)
    if parent_hierarchy is not None:
        path = parent_hierarchy.path
    else:
        path = delimiter + '1' + delimiter

    data = Hierarchies(
        # start new request feilds
        organisation_id=organisation_id,
        name=name,
        path=path,
        level=level,
        parent_id=parent_id,
        key_value=key_value,
        cached=bool(0)
        # end new request feilds
        # title=request.form.get("title")
    )
    db.session.add(data)
    
    db.session.commit()

    hierarchy_id = data.id
    
    if hierarchy_id != 1:
        data.path = data.path + str(hierarchy_id) + delimiter
    else:
        data.name = "All"
        data.parent_id = ''
        db.session.commit()

        data = Hierarchies(
            # start new request feilds
            organisation_id=organisation_id,
            name=name,
            path=path,
            level=level,
            parent_id=parent_id,
            key_value=key_value,
            cached=bool(0)
            # end new request feilds
            # title=request.form.get("title")
        )
        db.session.add(data)
        db.session.commit()
        data.path = data.path + str(hierarchy_id) + delimiter
    
    path = data.path

    level = fn.path_level(data.path)
    data.level = level

    current_hierarchy_ids = path.split('/')
    current_hierarchy_ids = current_hierarchy_ids[:] = [int(x) for x in current_hierarchy_ids if x]

    for current_hierarchy_id in current_hierarchy_ids:

        cache_data = Cache_hierarchies(
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
        db.session.add(cache_data)
    
    data.cached = bool(1)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errorInfo = e.orig.args
        flash(errorInfo[0], 'error')

    return redirect(url_for('hierarchies_admin.index')+"?organization="+g.organization)


@mod_admin_hierarchies.route('/show/<id>', methods=['GET'])
@mobile_template('{mobile/}hierarchies/admin/show.html')
# @login_required
def show(id,template):
    data = Hierarchies.query.get(id)

    return render_template(template, data=data)


@mod_admin_hierarchies.route('/edit/<id>', methods=['GET'])
@mobile_template('{mobile/}hierarchies/admin/edit.html')
# @login_required
def edit(id,template):

    # If in form is submitted
    form = HierarchiesForm(request.form)

    data = Hierarchies.query.get(id)

    parents = Hierarchies.query.all()

    return render_template(template, form=form, data=data, parents=parents)


@mod_admin_hierarchies.route('/update/<id>', methods=['PUT', 'PATCH', 'POST'])
# @login_required
def update(id):

    delimiter = '/'

    parent_id=request.form.get('parent_id')
    if parent_id is None or parent_id == '':
        parent_id = 1

    parent_hierarchy = Hierarchies.query.get(parent_id)
    if parent_hierarchy is not None:
        new_path = parent_hierarchy.path
    else:
        new_path = delimiter + '1' + delimiter
    
    data = Hierarchies.query.get(id)

    old_path = data.path

    hierarchy_id = data.id
    new_path = new_path + str(hierarchy_id) + delimiter

    # start update request feilds
    data.organisation_id = request.form.get('organisation_id')
    data.name = request.form.get('name')
    # data.path = new_path
    data.level = fn.path_level(data.path)
    data.parent_id = parent_id
    data.key_value = request.form.get('key_value')
    data.cached  = bool(0)
    # end update request feilds
    
    path_search = old_path + "%"
    update_hierarchies = Hierarchies.query.filter(Hierarchies.path.like(path_search))
    
    for hierarchy in update_hierarchies:
        hierarchy.path = hierarchy.path.replace(old_path,new_path)

        organisation_id = hierarchy.organisation_id
        hierarchy_id = hierarchy.id
        name = hierarchy.name
        path = hierarchy.path
        level = hierarchy.level
        parent_id = hierarchy.parent_id
        key_value = hierarchy.key_value

        current_hierarchy_ids = path.split('/')
        current_hierarchy_ids = current_hierarchy_ids[:] = [int(x) for x in current_hierarchy_ids if x]

        data = Cache_hierarchies.query.filter(Cache_hierarchies.hierarchy_id == hierarchy_id).all()
        for delete_data in data:
            db.session.delete(delete_data)

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

    return redirect(url_for('hierarchies_admin.index')+"?organization="+g.organization)


@mod_admin_hierarchies.route('/destroy/<id>', methods=['POST', 'DELETE', 'GET'])
# @login_required
def destroy(id):
    data = Hierarchies.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('hierarchies_admin.index')+"?organization="+g.organization)


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Hierarchies, "before_insert")
def before_insert(mapper, connection, target):
    pass


@event.listens_for(Hierarchies, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Hierarchies, "before_update")
def before_update(mapper, connection, target):
    pass


@event.listens_for(Hierarchies, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Hierarchies, "before_delete")
def before_delete(mapper, connection, target):
    pass


@event.listens_for(Hierarchies, "after_delete")
def after_delete(mapper, connection, target):
    pass
