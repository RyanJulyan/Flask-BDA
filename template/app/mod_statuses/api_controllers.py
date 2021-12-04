
import sys

# Import Flask Resource, fields from flask_restx for API and Swagger
from flask_restx import Resource, fields, reqparse
# Import sql functions (SUM,MIN,MAX,AVG)
from sqlalchemy.sql import func
# Import sql events 
from sqlalchemy import event, and_, or_

# JWT for API
from flask_jwt_extended import jwt_required

# Import the database object from the main app module
from app import db, app, api

# Import helper functions, comment in as needed (commented out for performance)
from app.mod_helper_functions import functions as fn

# Import statuses module models 
from app.mod_statuses.models import Statuses
# Import module models (e.g. User)


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
ns = api.namespace('api/statuses', description='Database model "Statuses", resource based, Api. \
    This API should have 9 endpoints from the name of the model prefixed by "api".\
    There are standard 5 CRUD APIs, a 2 BULK APIs, 1 Seed, and 1 Aggregate')

statuses = api.model('Statuses', {
    'id': fields.Integer(readonly=True, description='The Statuses unique identifier'),
    # start new add_argument
    'status_key': fields.String(required=True, description='The Statuses Status key'),
    'status_display_name': fields.String(required=True, description='The Statuses Status display name'),
    'status_description': fields.String(required=True, description='The Statuses Status description'),
    'status_group': fields.String(required=True, description='The Statuses Status group'),
    'key_value': fields.String(description='The Statuses Key value')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

statuses_agg = api.model('Statuses_agg', {
    # start new add_agg_argument
    'status_key_count': fields.Integer(readonly=True, description='The Statuses Status key count'),
    'status_display_name_count': fields.Integer(readonly=True, description='The Statuses Status display name count'),
    'status_description_count': fields.Integer(readonly=True, description='The Statuses Status description count'),
    'status_group_count': fields.Integer(readonly=True, description='The Statuses Status group count'),
    'key_value_count': fields.Integer(readonly=True, description='The Statuses Key value count')    # this line should be removed and replaced with the argumentAggParser variable
    # end new add_agg_argument
    # 'name_count': fields.String(required=True, description='The task count')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from Statuses into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# Statuses
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single statuses item, updates a single statuses item and lets you delete a statuses item

@ns.route('/<int:id>')
@ns.response(404, 'Statuses not found')
@ns.param('id', 'The Statuses identifier')
class StatusesResource(Resource):
    '''Show a single Statuses item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get statuses')
    @ns.marshal_list_with(statuses, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self, id):  # /statuses/<id>
        '''Fetch a single Statuses item given its identifier'''
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
                .get_or_404(id)
            )

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete statuses')
    @ns.doc(security='jwt')
    @jwt_required
    def delete(self, id):  # /statuses/<id>
        '''Delete a Statuses given its identifier'''
        data = Statuses.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Statuses Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update statuses')
    @ns.expect(statuses)
    @ns.marshal_list_with(statuses, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self, id):  # /statuses/<id>
        '''Update a Statuses given its identifier'''
        data = Statuses.query.get_or_404(id)
        # start update api_request feilds
        data.status_key = api.payload['status_key']
        data.status_display_name = api.payload['status_display_name']
        data.status_description = api.payload['status_description']
        data.status_group = api.payload['status_group']
        data.key_value = api.payload['key_value']
        # end update api_request feilds
        # data.title = api.payload['title']
        db.session.commit()
        return data, 201


# StatusesList
# shows a list of all Statuses, and lets you POST to add new Statuses
@ns.route('/')
class StatusesListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get statuses')
    @ns.expect(parser)
    @ns.marshal_list_with(statuses, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /statuses
        '''List Statuses records '''
        args = parser.parse_args()
        page = args['page']

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
                .items
            )

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert statuses')
    @ns.expect(statuses)
    @ns.marshal_with(statuses, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /statuses
        '''Create a new Statuses record'''
        data = Statuses(
            # start new api_request feilds
            status_key=api.payload['status_key'],
            status_display_name=api.payload['status_display_name'],
            status_description=api.payload['status_description'],
            status_group=api.payload['status_group'],
            key_value=api.payload['key_value']
            # end new api_request feilds
            # title = api.payload['title']
        )
        db.session.add(data)
        db.session.commit()
        return data, 201


# StatusesBulk
# Inserts and updates in Bulk of Statuses, and lets you POST to add and put to update new Statuses
@ns.route('/bulk')
class StatusesBulkListResource(Resource):
    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update statuses')
    @ns.expect(statuses)
    @ns.marshal_list_with(statuses, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self):  # /statuses/bulk
        '''Bulk update Statuses given their identifiers'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_update_mappings(Statuses,data)
        db.session.commit()
        return data, 201

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert statuses')
    @ns.expect(statuses)
    @ns.marshal_with(statuses, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /statuses/bulk
        '''Bulk create new Statuses records'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_insert_mappings(Statuses,data)
        db.session.commit()
        return data, 201


# StatusesSeed Data
# Inserts and updates in Bulk of Statuses, and lets you POST to add and put to update new Statuses
@ns.route('/seed/<int:level>')
class StatusesBulkSeedResource(Resource):
    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='seed statuses')
    # @ns.expect(statuses)
    # @ns.marshal_with(statuses, code=201)
    # @ns.doc(security='jwt')
    @ns.doc(security=None)
    # @jwt_required
    def get(self, level):  # /statuses/seed/<level>
        '''Seed bulk Statuses records. Level 1 = `Core` Data, Level 2 = `Nice to Have` Data, Level 3 = `Demo` Data'''
        data = {
            1:[
                {
                    'id':1,
                    'status_key':'new',
                    'status_display_name':'New',
                    'status_description':'A New Record or Entry has been created',
                    'status_group':'core',
                },
                {
                    'id':2,
                    'status_key':'active',
                    'status_display_name':'Active',
                    'status_description':'This Record or Entry is currently in an Active state',
                    'status_group':'core',
                },
                {
                    'id':3,
                    'status_key':'inactive',
                    'status_display_name':'Inactive',
                    'status_description':'This Record or Entry is currently in an Inctive state',
                    'status_group':'core',
                },
                {
                    'id':4,
                    'status_key':'deleted',
                    'status_display_name':'Deleted',
                    'status_description':'This Record or Entry has been Deleted',
                    'status_group':'core',
                },
                {
                    'id':5,
                    'status_key':'error',
                    'status_display_name':'Error',
                    'status_description':'The Current Record or Entry has raised an Error',
                    'status_group':'system',
                },
                {
                    'id':6,
                    'status_key':'failed',
                    'status_display_name':'Failed',
                    'status_description':'The Current Record or Entry has Failed to process',
                    'status_group':'system',
                },
                {
                    'id':7,
                    'status_key':'cancelled',
                    'status_display_name':'Cancelled',
                    'status_description':'This Record or Entry is currently in a Cancelled state',
                    'status_group':'core',
                },
                {
                    'id':8,
                    'status_key':'on_hold',
                    'status_display_name':'On Hold',
                    'status_description':'This Record or Entry is currently On Hold',
                    'status_group':'system',
                },
                {
                    'id':9,
                    'status_key':'processing',
                    'status_display_name':'Processing',
                    'status_description':'This Record or Entry is currently Processing',
                    'status_group':'system',
                },
                {
                    'id':10,
                    'status_key':'Completed',
                    'status_display_name':'Completed',
                    'status_description':'The Current Record or Entry has Completed a process',
                    'status_group':'core',
                },
            ],
            2:[
                {
                    'id':1,
                    'status_key':'new',
                    'status_display_name':'New',
                    'status_description':'A New Record or Entry has been created',
                    'status_group':'core',
                },
                {
                    'id':2,
                    'status_key':'active',
                    'status_display_name':'Active',
                    'status_description':'This Record or Entry is currently in an Active state',
                    'status_group':'core',
                },
                {
                    'id':3,
                    'status_key':'inactive',
                    'status_display_name':'Inactive',
                    'status_description':'This Record or Entry is currently in an Inctive state',
                    'status_group':'core',
                },
                {
                    'id':4,
                    'status_key':'deleted',
                    'status_display_name':'Deleted',
                    'status_description':'This Record or Entry has been Deleted',
                    'status_group':'core',
                },
                {
                    'id':5,
                    'status_key':'error',
                    'status_display_name':'Error',
                    'status_description':'The Current Record or Entry has raised an Error',
                    'status_group':'system',
                },
                {
                    'id':6,
                    'status_key':'failed',
                    'status_display_name':'Failed',
                    'status_description':'The Current Record or Entry has Failed to process',
                    'status_group':'system',
                },
                {
                    'id':7,
                    'status_key':'cancelled',
                    'status_display_name':'Cancelled',
                    'status_description':'This Record or Entry is currently in a Cancelled state',
                    'status_group':'core',
                },
                {
                    'id':8,
                    'status_key':'on_hold',
                    'status_display_name':'On Hold',
                    'status_description':'This Record or Entry is currently On Hold',
                    'status_group':'system',
                },
                {
                    'id':9,
                    'status_key':'processing',
                    'status_display_name':'Processing',
                    'status_description':'This Record or Entry is currently Processing',
                    'status_group':'system',
                },
                {
                    'id':10,
                    'status_key':'Completed',
                    'status_display_name':'Completed',
                    'status_description':'The Current Record or Entry has Completed a process',
                    'status_group':'core',
                },
            ],
            3:[
                {
                    'id':1,
                    'status_key':'new',
                    'status_display_name':'New',
                    'status_description':'A New Record or Entry has been created',
                    'status_group':'core',
                },
                {
                    'id':2,
                    'status_key':'active',
                    'status_display_name':'Active',
                    'status_description':'This Record or Entry is currently in an Active state',
                    'status_group':'core',
                },
                {
                    'id':3,
                    'status_key':'inactive',
                    'status_display_name':'Inactive',
                    'status_description':'This Record or Entry is currently in an Inctive state',
                    'status_group':'core',
                },
                {
                    'id':4,
                    'status_key':'deleted',
                    'status_display_name':'Deleted',
                    'status_description':'This Record or Entry has been Deleted',
                    'status_group':'core',
                },
                {
                    'id':5,
                    'status_key':'error',
                    'status_display_name':'Error',
                    'status_description':'The Current Record or Entry has raised an Error',
                    'status_group':'system',
                },
                {
                    'id':6,
                    'status_key':'failed',
                    'status_display_name':'Failed',
                    'status_description':'The Current Record or Entry has Failed to process',
                    'status_group':'system',
                },
                {
                    'id':7,
                    'status_key':'cancelled',
                    'status_display_name':'Cancelled',
                    'status_description':'This Record or Entry is currently in a Cancelled state',
                    'status_group':'core',
                },
                {
                    'id':8,
                    'status_key':'on_hold',
                    'status_display_name':'On Hold',
                    'status_description':'This Record or Entry is currently On Hold',
                    'status_group':'system',
                },
                {
                    'id':9,
                    'status_key':'processing',
                    'status_display_name':'Processing',
                    'status_description':'This Record or Entry is currently Processing',
                    'status_group':'system',
                },
                {
                    'id':10,
                    'status_key':'Completed',
                    'status_display_name':'Completed',
                    'status_description':'The Current Record or Entry has Completed a process',
                    'status_group':'core',
                },
            ]
        }
        
        data = json.dumps(data[level])
        
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        try:
            db.session.bulk_insert_mappings(Statuses,data)
            db.session.commit()
        
            return data, 201
        except:
            return [{"error":str(sys.exc_info()[0]),"details":str(sys.exc_info()[1])}],500


# StatusesAggregate
# shows a list of all Statuses, and lets you POST to add new Statuses
@ns.route('/aggregate')
class StatusesAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get statuses aggregates')
    @ns.marshal_with(statuses_agg, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /statuses
        '''Aggregate Statuses records '''

        data = Statuses.query.with_entities(
            
            # start new api_aggregate feilds

                func.count(Statuses.status_key).label('status_key_count'),

                func.count(Statuses.status_display_name).label('status_display_name_count'),

                func.count(Statuses.status_description).label('status_description_count'),

                func.count(Statuses.status_group).label('status_group_count'),

                func.count(Statuses.key_value).label('key_value_count')
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds

                "status_key_count":data.status_key_count,

                "status_display_name_count":data.status_display_name_count,

                "status_description_count":data.status_description_count,

                "status_group_count":data.status_group_count,

                "key_value_count":data.key_value_count
            # end new api_aggregate_object feilds
        }

        return data_obj, 200


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Statuses, "before_insert")
def before_insert(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Statuses",
            action="Before Insert",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'statuses', run_type = "before_insert", data = data, convert_sqlalchemy_to_json = False)

    pass


@event.listens_for(Statuses, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Statuses, "before_update")
def before_update(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Statuses",
            action="Before Update",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'statuses', run_type = "before_insert", data = data, convert_sqlalchemy_to_json = False)
        
    pass


@event.listens_for(Statuses, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Statuses, "before_delete")
def before_delete(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Statuses",
            action="Before Delete",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'statuses', run_type = "before_insert", data = data, convert_sqlalchemy_to_json = False)
        
    pass


@event.listens_for(Statuses, "after_delete")
def after_delete(mapper, connection, target):
    pass
