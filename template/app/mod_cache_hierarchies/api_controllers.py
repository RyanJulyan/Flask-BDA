
# Import Flask Resource, fields from flask_restx for API and Swagger
from flask_restx import Resource, fields, reqparse
# Import sql functions (SUM,MIN,MAX,AVG)
from sqlalchemy.sql import func
# Import sql events 
from sqlalchemy import event

# JWT for API
from flask_jwt_extended import jwt_required

# Import the database object from the main app module
from app import db, app, api

# Import helper functions, comment in as needed (commented out for performance)
# from app.mod_helper_functions import functions as fn

# Import module models (i.e. User)
from app.mod_cache_hierarchies.models import Cache_hierarchies

# Import json for consuming payload and for payload data type transformations
import json

# Import read_json from pandas for payload data type transformations
from pandas import read_json

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


# Swagger namespace
ns = api.namespace('api/cache_hierarchies', description='Database model "Cache_hierarchies", resource based, Api. \
    This API should have 2 endpoints from the name of the model prefixed by "api".')

cache_hierarchies = api.model('Cache_hierarchies', {
    'id': fields.Integer(readonly=True, description='The Cache_hierarchies unique identifier'),
    # start new add_argument
    'organisation_id': fields.Float(required=True, description='The Cache_hierarchies Organisation id'),
    'current_hierarchy_id': fields.Float(required=True, description='The Cache_hierarchies Current hierarchy id'),
    'hierarchy_id': fields.Float(required=True, description='The Cache_hierarchies Hierarchy id'),
    'name': fields.String(required=True, description='The Cache_hierarchies Name'),
    'path': fields.String(required=True, description='The Cache_hierarchies Path'),
    'level': fields.Float(description='The Cache_hierarchies Level'),
    'parent_id': fields.Float(description='The Cache_hierarchies Parent id'),
    'key_value': fields.String(description='The Cache_hierarchies Key value')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

cache_hierarchies_agg = api.model('Cache_hierarchies_agg', {
    # start new add_agg_argument
    'organisation_id_count': fields.Integer(readonly=True, description='The Cache_hierarchies Organisation id count'),
    'organisation_id_sum': fields.Float(readonly=True, description='The Cache_hierarchies Organisation id sum'),
    'organisation_id_avg': fields.Float(readonly=True, description='The Cache_hierarchies Organisation id avg'),
    'organisation_id_min': fields.Float(readonly=True, description='The Cache_hierarchies Organisation id min'),
    'organisation_id_max': fields.Float(readonly=True, description='The Cache_hierarchies Organisation id max'),
    'current_hierarchy_id_count': fields.Integer(readonly=True, description='The Cache_hierarchies Current hierarchy id count'),
    'current_hierarchy_id_sum': fields.Float(readonly=True, description='The Cache_hierarchies Current hierarchy id sum'),
    'current_hierarchy_id_avg': fields.Float(readonly=True, description='The Cache_hierarchies Current hierarchy id avg'),
    'current_hierarchy_id_min': fields.Float(readonly=True, description='The Cache_hierarchies Current hierarchy id min'),
    'current_hierarchy_id_max': fields.Float(readonly=True, description='The Cache_hierarchies Current hierarchy id max'),
    'hierarchy_id_count': fields.Integer(readonly=True, description='The Cache_hierarchies Hierarchy id count'),
    'hierarchy_id_sum': fields.Float(readonly=True, description='The Cache_hierarchies Hierarchy id sum'),
    'hierarchy_id_avg': fields.Float(readonly=True, description='The Cache_hierarchies Hierarchy id avg'),
    'hierarchy_id_min': fields.Float(readonly=True, description='The Cache_hierarchies Hierarchy id min'),
    'hierarchy_id_max': fields.Float(readonly=True, description='The Cache_hierarchies Hierarchy id max'),
    'name_count': fields.Integer(readonly=True, description='The Cache_hierarchies Name count'),
    'path_count': fields.Integer(readonly=True, description='The Cache_hierarchies Path count'),
    'level_count': fields.Integer(readonly=True, description='The Cache_hierarchies Level count'),
    'level_sum': fields.Float(readonly=True, description='The Cache_hierarchies Level sum'),
    'level_avg': fields.Float(readonly=True, description='The Cache_hierarchies Level avg'),
    'level_min': fields.Float(readonly=True, description='The Cache_hierarchies Level min'),
    'level_max': fields.Float(readonly=True, description='The Cache_hierarchies Level max'),
    'parent_id_count': fields.Integer(readonly=True, description='The Cache_hierarchies Parent id count'),
    'parent_id_sum': fields.Float(readonly=True, description='The Cache_hierarchies Parent id sum'),
    'parent_id_avg': fields.Float(readonly=True, description='The Cache_hierarchies Parent id avg'),
    'parent_id_min': fields.Float(readonly=True, description='The Cache_hierarchies Parent id min'),
    'parent_id_max': fields.Float(readonly=True, description='The Cache_hierarchies Parent id max'),
    'key_value_count': fields.Integer(readonly=True, description='The Cache_hierarchies Key value count')    # this line should be removed and replaced with the argumentAggParser variable
    # end new add_agg_argument
    # 'name_count': fields.String(required=True, description='The task count')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from Cache_hierarchies into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# Cache_hierarchies
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single cache_hierarchies item, updates a single cache_hierarchies item and lets you delete a cache_hierarchies item

@ns.route('/<int:id>')
@ns.response(404, 'Cache_hierarchies not found')
@ns.param('id', 'The Cache_hierarchies identifier')
class Cache_hierarchiesResource(Resource):
    '''Show a single Cache_hierarchies item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get cache_hierarchies')
    @ns.marshal_list_with(cache_hierarchies, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self, id):  # /cache_hierarchies/<id>
        '''Fetch a single Cache_hierarchies item given its identifier'''
        data = Cache_hierarchies.query.get_or_404(id)

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete cache_hierarchies')
    @ns.doc(security='jwt')
    @jwt_required
    def delete(self, id):  # /cache_hierarchies/<id>
        '''Delete a Cache_hierarchies given its identifier'''
        data = Cache_hierarchies.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Cache_hierarchies Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update cache_hierarchies')
    @ns.expect(cache_hierarchies)
    @ns.marshal_list_with(cache_hierarchies, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self, id):  # /cache_hierarchies/<id>
        '''Update a Cache_hierarchies given its identifier'''
        data = Cache_hierarchies.query.get_or_404(id)
        # start update api_request feilds
        data.organisation_id = api.payload['organisation_id']
        data.current_hierarchy_id = api.payload['current_hierarchy_id']
        data.hierarchy_id = api.payload['hierarchy_id']
        data.name = api.payload['name']
        data.path = api.payload['path']
        data.level = api.payload['level']
        data.parent_id = api.payload['parent_id']
        data.key_value = api.payload['key_value']
        # end update api_request feilds
        # data.title = api.payload['title']
        db.session.commit()
        return data, 201


# Cache_hierarchiesList
# shows a list of all Cache_hierarchies, and lets you POST to add new Cache_hierarchies
@ns.route('/')
class Cache_hierarchiesListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get cache_hierarchies')
    @ns.expect(parser)
    @ns.marshal_list_with(cache_hierarchies, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /cache_hierarchies
        '''List Cache_hierarchies records '''
        args = parser.parse_args()
        page = args['page']

        data = Cache_hierarchies.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE']).items

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert cache_hierarchies')
    @ns.expect(cache_hierarchies)
    @ns.marshal_with(cache_hierarchies, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /cache_hierarchies
        '''Create a new Cache_hierarchies record'''
        data = Cache_hierarchies(
            # start new api_request feilds
            organisation_id=api.payload['organisation_id'],
            current_hierarchy_id=api.payload['current_hierarchy_id'],
            hierarchy_id=api.payload['hierarchy_id'],
            name=api.payload['name'],
            path=api.payload['path'],
            level=api.payload['level'],
            parent_id=api.payload['parent_id'],
            key_value=api.payload['key_value']
            # end new api_request feilds
            # title = api.payload['title']
        )
        db.session.add(data)
        db.session.commit()
        return data, 201


# Cache_hierarchiesBulk
# Inserts and updates in Bulk of Cache_hierarchies, and lets you POST to add and put to update new Cache_hierarchies
@ns.route('/bulk')
class Cache_hierarchiesBulkListResource(Resource):
    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update cache_hierarchies')
    @ns.expect(cache_hierarchies)
    @ns.marshal_list_with(cache_hierarchies, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self):  # /cache_hierarchies/bulk
        '''Bulk update Cache_hierarchies given their identifiers'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_update_mappings(Cache_hierarchies,data)
        db.session.commit()
        return data, 201

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert cache_hierarchies')
    @ns.expect(cache_hierarchies)
    @ns.marshal_with(cache_hierarchies, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /cache_hierarchies/bulk
        '''Bulk create new Cache_hierarchies records'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_insert_mappings(Cache_hierarchies,data)
        db.session.commit()
        return data, 201


# Cache_hierarchiesSeed Data
# Inserts and updates in Bulk of Cache_hierarchies, and lets you POST to add and put to update new Cache_hierarchies
@ns.route('/seed/<int:level>')
class Cache_hierarchiesBulkListResource(Resource):
    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='seed cache_hierarchies')
    @ns.expect(cache_hierarchies)
    @ns.marshal_with(cache_hierarchies, code=201)
    # @ns.doc(security='jwt')
    @ns.doc(security=None)
    # @jwt_required
    def get(self, level):  # /cache_hierarchies/seed/<level>
        '''Seed bulk Cache_hierarchies records. Level 1 = `Core` Data, Level 2 = `Nice to Have` Data, Level 3 = `Demo` Data'''
        data = {
            1:[
                {}, ## Insert `Core` data to seed into this object
                {} ## create more objects as needed
            ],
            2:[
                {}, ## Insert `Nice to Have` Data to seed into this object
                {} ## create more objects as needed
            ],
            3:[
                {}, ## Insert `Demo` Data to seed into this object
                {} ## create more objects as needed
            ]
        }
        
        data = json.dumps(data[level])
        
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_insert_mappings(Cache_hierarchies,data)
        db.session.commit()
        return data, 201


# Cache_hierarchiesAggregate
# shows a list of all Cache_hierarchies, and lets you POST to add new Cache_hierarchies
@ns.route('/aggregate')
class Cache_hierarchiesAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get cache_hierarchies aggregates')
    @ns.marshal_with(cache_hierarchies_agg, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /cache_hierarchies
        '''Aggregate Cache_hierarchies records '''

        data = Cache_hierarchies.query.with_entities(
            
            # start new api_aggregate feilds

                func.count(Cache_hierarchies.organisation_id).label('organisation_id_count'),

                func.sum(Cache_hierarchies.organisation_id).label('organisation_id_sum'),

                func.avg(Cache_hierarchies.organisation_id).label('organisation_id_avg'),

                func.min(Cache_hierarchies.organisation_id).label('organisation_id_min'),

                func.max(Cache_hierarchies.organisation_id).label('organisation_id_max'),
                func.count(Cache_hierarchies.current_hierarchy_id).label('current_hierarchy_id_count'),

                func.sum(Cache_hierarchies.current_hierarchy_id).label('current_hierarchy_id_sum'),

                func.avg(Cache_hierarchies.current_hierarchy_id).label('current_hierarchy_id_avg'),

                func.min(Cache_hierarchies.current_hierarchy_id).label('current_hierarchy_id_min'),

                func.max(Cache_hierarchies.current_hierarchy_id).label('current_hierarchy_id_max'),
                func.count(Cache_hierarchies.hierarchy_id).label('hierarchy_id_count'),

                func.sum(Cache_hierarchies.hierarchy_id).label('hierarchy_id_sum'),

                func.avg(Cache_hierarchies.hierarchy_id).label('hierarchy_id_avg'),

                func.min(Cache_hierarchies.hierarchy_id).label('hierarchy_id_min'),

                func.max(Cache_hierarchies.hierarchy_id).label('hierarchy_id_max'),
                func.count(Cache_hierarchies.name).label('name_count'),

                func.count(Cache_hierarchies.path).label('path_count'),

                func.count(Cache_hierarchies.level).label('level_count'),

                func.sum(Cache_hierarchies.level).label('level_sum'),

                func.avg(Cache_hierarchies.level).label('level_avg'),

                func.min(Cache_hierarchies.level).label('level_min'),

                func.max(Cache_hierarchies.level).label('level_max'),
                func.count(Cache_hierarchies.parent_id).label('parent_id_count'),

                func.sum(Cache_hierarchies.parent_id).label('parent_id_sum'),

                func.avg(Cache_hierarchies.parent_id).label('parent_id_avg'),

                func.min(Cache_hierarchies.parent_id).label('parent_id_min'),

                func.max(Cache_hierarchies.parent_id).label('parent_id_max'),
                func.count(Cache_hierarchies.key_value).label('key_value_count')
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds

                "organisation_id_count":data.organisation_id_count,

                "organisation_id_sum":data.organisation_id_sum,

                "organisation_id_avg":data.organisation_id_avg,

                "organisation_id_min":data.organisation_id_min,

                "organisation_id_max":data.organisation_id_max,

                "current_hierarchy_id_count":data.current_hierarchy_id_count,

                "current_hierarchy_id_sum":data.current_hierarchy_id_sum,

                "current_hierarchy_id_avg":data.current_hierarchy_id_avg,

                "current_hierarchy_id_min":data.current_hierarchy_id_min,

                "current_hierarchy_id_max":data.current_hierarchy_id_max,

                "hierarchy_id_count":data.hierarchy_id_count,

                "hierarchy_id_sum":data.hierarchy_id_sum,

                "hierarchy_id_avg":data.hierarchy_id_avg,

                "hierarchy_id_min":data.hierarchy_id_min,

                "hierarchy_id_max":data.hierarchy_id_max,

                "name_count":data.name_count,

                "path_count":data.path_count,

                "level_count":data.level_count,

                "level_sum":data.level_sum,

                "level_avg":data.level_avg,

                "level_min":data.level_min,

                "level_max":data.level_max,

                "parent_id_count":data.parent_id_count,

                "parent_id_sum":data.parent_id_sum,

                "parent_id_avg":data.parent_id_avg,

                "parent_id_min":data.parent_id_min,

                "parent_id_max":data.parent_id_max,

                "key_value_count":data.key_value_count
            # end new api_aggregate_object feilds
        }

        return data_obj, 200


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Cache_hierarchies, "before_insert")
def before_insert(mapper, connection, target):
    pass


@event.listens_for(Cache_hierarchies, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Cache_hierarchies, "before_update")
def before_update(mapper, connection, target):
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
