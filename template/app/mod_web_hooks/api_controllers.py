
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

# Import web_hooks module models 
from app.mod_web_hooks.models import Web_hooks
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
ns = api.namespace('api/web_hooks', description='Database model "Web_hooks", resource based, Api. \
    This API should have 9 endpoints from the name of the model prefixed by "api".\
    There are standard 5 CRUD APIs, a 2 BULK APIs, 1 Seed, and 1 Aggregate')

web_hooks = api.model('Web_hooks', {
    'id': fields.Integer(readonly=True, description='The Web_hooks unique identifier'),
    # start new add_argument
    'webhook_name': fields.String(required=True, description='The Web_hooks Webhook name'),
    'run_in_module_name': fields.String(required=True, description='The Web_hooks Run in module name'),
    'run_before_insert': fields.String(required=True, description='The Web_hooks Run before insert'),
    'run_after_insert': fields.String(required=True, description='The Web_hooks Run after insert'),
    'run_before_update': fields.String(required=True, description='The Web_hooks Run before update'),
    'run_after_update': fields.String(required=True, description='The Web_hooks Run after update'),
    'run_before_delete': fields.String(required=True, description='The Web_hooks Run before delete'),
    'run_after_delete': fields.String(required=True, description='The Web_hooks Run after delete'),
    'method': fields.String(required=True, description='The Web_hooks Method'),
    'data_type': fields.String(required=True, description='The Web_hooks Data type'),
    'api_endpoint': fields.String(required=True, description='The Web_hooks Api endpoint'),
    'api_headers': fields.String(description='The Web_hooks Api headers'),
    'api_params': fields.String(description='The Web_hooks Api params'),
    'active_flag': fields.String(required=True, description='The Web_hooks Active flag')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

web_hooks_agg = api.model('Web_hooks_agg', {
    # start new add_agg_argument
    'webhook_name_count': fields.Integer(readonly=True, description='The Web_hooks Webhook name count'),
    'run_in_module_name_count': fields.Integer(readonly=True, description='The Web_hooks Run in module name count'),
    'run_before_insert_count': fields.Integer(readonly=True, description='The Web_hooks Run before insert count'),
    'run_after_insert_count': fields.Integer(readonly=True, description='The Web_hooks Run after insert count'),
    'run_before_update_count': fields.Integer(readonly=True, description='The Web_hooks Run before update count'),
    'run_after_update_count': fields.Integer(readonly=True, description='The Web_hooks Run after update count'),
    'run_before_delete_count': fields.Integer(readonly=True, description='The Web_hooks Run before delete count'),
    'run_after_delete_count': fields.Integer(readonly=True, description='The Web_hooks Run after delete count'),
    'method_count': fields.Integer(readonly=True, description='The Web_hooks Method count'),
    'data_type_count': fields.Integer(readonly=True, description='The Web_hooks Data type count'),
    'api_endpoint_count': fields.Integer(readonly=True, description='The Web_hooks Api endpoint count'),
    'api_headers_count': fields.Integer(readonly=True, description='The Web_hooks Api headers count'),
    'api_params_count': fields.Integer(readonly=True, description='The Web_hooks Api params count'),
    'active_flag_count': fields.Integer(readonly=True, description='The Web_hooks Active flag count')    # this line should be removed and replaced with the argumentAggParser variable
    # end new add_agg_argument
    # 'name_count': fields.String(required=True, description='The task count')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from Web_hooks into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# Web_hooks
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single web_hooks item, updates a single web_hooks item and lets you delete a web_hooks item

@ns.route('/<int:id>')
@ns.response(404, 'Web_hooks not found')
@ns.param('id', 'The Web_hooks identifier')
class Web_hooksResource(Resource):
    '''Show a single Web_hooks item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get web_hooks')
    @ns.marshal_list_with(web_hooks, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self, id):  # /web_hooks/<id>
        '''Fetch a single Web_hooks item given its identifier'''
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
                .get_or_404(id)
            )

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete web_hooks')
    @ns.doc(security='jwt')
    @jwt_required
    def delete(self, id):  # /web_hooks/<id>
        '''Delete a Web_hooks given its identifier'''
        data = Web_hooks.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Web_hooks Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update web_hooks')
    @ns.expect(web_hooks)
    @ns.marshal_list_with(web_hooks, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self, id):  # /web_hooks/<id>
        '''Update a Web_hooks given its identifier'''
        data = Web_hooks.query.get_or_404(id)
        # start update api_request feilds
        data.webhook_name = api.payload['webhook_name']
        data.run_in_module_name = api.payload['run_in_module_name']
        data.run_before_insert = api.payload['run_before_insert']
        data.run_after_insert = api.payload['run_after_insert']
        data.run_before_update = api.payload['run_before_update']
        data.run_after_update = api.payload['run_after_update']
        data.run_before_delete = api.payload['run_before_delete']
        data.run_after_delete = api.payload['run_after_delete']
        data.method = api.payload['method']
        data.data_type = api.payload['data_type']
        data.api_endpoint = api.payload['api_endpoint']
        data.api_headers = api.payload['api_headers']
        data.api_params = api.payload['api_params']
        data.active_flag = api.payload['active_flag']
        # end update api_request feilds
        # data.title = api.payload['title']
        db.session.commit()
        return data, 201


# Web_hooksList
# shows a list of all Web_hooks, and lets you POST to add new Web_hooks
@ns.route('/')
class Web_hooksListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get web_hooks')
    @ns.expect(parser)
    @ns.marshal_list_with(web_hooks, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /web_hooks
        '''List Web_hooks records '''
        args = parser.parse_args()
        page = args['page']

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
                .items
            )

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert web_hooks')
    @ns.expect(web_hooks)
    @ns.marshal_with(web_hooks, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /web_hooks
        '''Create a new Web_hooks record'''
        data = Web_hooks(
            # start new api_request feilds
            webhook_name=api.payload['webhook_name'],
            run_in_module_name=api.payload['run_in_module_name'],
            run_before_insert=api.payload['run_before_insert'],
            run_after_insert=api.payload['run_after_insert'],
            run_before_update=api.payload['run_before_update'],
            run_after_update=api.payload['run_after_update'],
            run_before_delete=api.payload['run_before_delete'],
            run_after_delete=api.payload['run_after_delete'],
            method=api.payload['method'],
            data_type=api.payload['data_type'],
            api_endpoint=api.payload['api_endpoint'],
            api_headers=api.payload['api_headers'],
            api_params=api.payload['api_params'],
            active_flag=api.payload['active_flag']
            # end new api_request feilds
            # title = api.payload['title']
        )
        db.session.add(data)
        db.session.commit()
        return data, 201


# Web_hooksBulk
# Inserts and updates in Bulk of Web_hooks, and lets you POST to add and put to update new Web_hooks
@ns.route('/bulk')
class Web_hooksBulkListResource(Resource):
    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update web_hooks')
    @ns.expect(web_hooks)
    @ns.marshal_list_with(web_hooks, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self):  # /web_hooks/bulk
        '''Bulk update Web_hooks given their identifiers'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_update_mappings(Web_hooks,data)
        db.session.commit()
        return data, 201

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert web_hooks')
    @ns.expect(web_hooks)
    @ns.marshal_with(web_hooks, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /web_hooks/bulk
        '''Bulk create new Web_hooks records'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_insert_mappings(Web_hooks,data)
        db.session.commit()
        return data, 201


# Web_hooksSeed Data
# Inserts and updates in Bulk of Web_hooks, and lets you POST to add and put to update new Web_hooks
@ns.route('/seed/<int:level>')
class Web_hooksBulkSeedResource(Resource):
    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='seed web_hooks')
    # @ns.expect(web_hooks)
    # @ns.marshal_with(web_hooks, code=201)
    # @ns.doc(security='jwt')
    @ns.doc(security=None)
    # @jwt_required
    def post(self, level):  # /web_hooks/seed/<level>
        '''Seed bulk Web_hooks records. Level 1 = `Core` Data, Level 2 = `Nice to Have` Data, Level 3 = `Demo` Data'''
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
        db.session.bulk_insert_mappings(Web_hooks,data)
        db.session.commit()
        return data, 201


# Web_hooksAggregate
# shows a list of all Web_hooks, and lets you POST to add new Web_hooks
@ns.route('/aggregate')
class Web_hooksAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get web_hooks aggregates')
    @ns.marshal_with(web_hooks_agg, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /web_hooks
        '''Aggregate Web_hooks records '''

        data = Web_hooks.query.with_entities(
            
            # start new api_aggregate feilds

                func.count(Web_hooks.webhook_name).label('webhook_name_count'),

                func.count(Web_hooks.run_in_module_name).label('run_in_module_name_count'),

                func.count(Web_hooks.run_before_insert).label('run_before_insert_count'),

                func.count(Web_hooks.run_after_insert).label('run_after_insert_count'),

                func.count(Web_hooks.run_before_update).label('run_before_update_count'),

                func.count(Web_hooks.run_after_update).label('run_after_update_count'),

                func.count(Web_hooks.run_before_delete).label('run_before_delete_count'),

                func.count(Web_hooks.run_after_delete).label('run_after_delete_count'),

                func.count(Web_hooks.method).label('method_count'),

                func.count(Web_hooks.data_type).label('data_type_count'),

                func.count(Web_hooks.api_endpoint).label('api_endpoint_count'),

                func.count(Web_hooks.api_headers).label('api_headers_count'),

                func.count(Web_hooks.api_params).label('api_params_count'),

                func.count(Web_hooks.active_flag).label('active_flag_count')
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds

                "webhook_name_count":data.webhook_name_count,

                "run_in_module_name_count":data.run_in_module_name_count,

                "run_before_insert_count":data.run_before_insert_count,

                "run_after_insert_count":data.run_after_insert_count,

                "run_before_update_count":data.run_before_update_count,

                "run_after_update_count":data.run_after_update_count,

                "run_before_delete_count":data.run_before_delete_count,

                "run_after_delete_count":data.run_after_delete_count,

                "method_count":data.method_count,

                "data_type_count":data.data_type_count,

                "api_endpoint_count":data.api_endpoint_count,

                "api_headers_count":data.api_headers_count,

                "api_params_count":data.api_params_count,

                "active_flag_count":data.active_flag_count
            # end new api_aggregate_object feilds
        }

        return data_obj, 200


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Web_hooks, "before_insert")
def before_insert(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Web_hooks",
            action="Before Insert",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Web_hooks, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Web_hooks, "before_update")
def before_update(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Web_hooks",
            action="Before Update",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Web_hooks, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Web_hooks, "before_delete")
def before_delete(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Web_hooks",
            action="Before Delete",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Web_hooks, "after_delete")
def after_delete(mapper, connection, target):
    pass
