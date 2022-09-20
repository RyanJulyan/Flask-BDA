
# Import json for consuming payload and for payload data type transformations
import json

# Import read_json from pandas for payload data type transformations
from pandas import read_json

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


# Swagger namespace
ns = api.namespace('api/api_keys', description='Database model "Api_keys", resource based, Api. \
    This API should have 9 endpoints from the name of the model prefixed by "api".\
    There are standard 5 CRUD APIs, a 2 BULK APIs, 1 Seed, and 1 Aggregate')

api_keys = api.model('Api_keys', {
    'id': fields.Integer(readonly=True, description='The Api_keys unique identifier'),
    # start new add_argument
    'api_key': fields.String(required=True, description='The Api_keys Api key'),
    'api_key_notes': fields.String(description='The Api_keys Api key notes'),
    'created_user_id': fields.Float(required=True, description='The Api_keys Created user id'),
    'valid_from': fields.String(required=True, description='The Api_keys Valid from'),
    'valid_to': fields.String(required=True, description='The Api_keys Valid to')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

api_keys_agg = api.model('Api_keys_agg', {
    # start new add_agg_argument
    'api_key_count': fields.Integer(readonly=True, description='The Api_keys Api key count'),
    'api_key_notes_count': fields.Integer(readonly=True, description='The Api_keys Api key notes count'),
    'created_user_id_count': fields.Integer(readonly=True, description='The Api_keys Created user id count'),
    'created_user_id_sum': fields.Float(readonly=True, description='The Api_keys Created user id sum'),
    'created_user_id_avg': fields.Float(readonly=True, description='The Api_keys Created user id avg'),
    'created_user_id_min': fields.Float(readonly=True, description='The Api_keys Created user id min'),
    'created_user_id_max': fields.Float(readonly=True, description='The Api_keys Created user id max'),
    'valid_from_count': fields.Integer(readonly=True, description='The Api_keys Valid from count'),
    'valid_to_count': fields.Integer(readonly=True, description='The Api_keys Valid to count')    # this line should be removed and replaced with the argumentAggParser variable
    # end new add_agg_argument
    # 'name_count': fields.String(required=True, description='The task count')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from Api_keys into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# Api_keys
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single api_keys item, updates a single api_keys item and lets you delete a api_keys item

@ns.route('/<int:id>')
@ns.response(404, 'Api_keys not found')
@ns.param('id', 'The Api_keys identifier')
class Api_keysResource(Resource):
    '''Show a single Api_keys item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get api_keys')
    @ns.marshal_list_with(api_keys, code=200)
    @ns.doc(security='jwt')
    # @jwt_required
    def get(self, id):  # /api_keys/<id>
        '''Fetch a single Api_keys item given its identifier'''
        data = (
                Api_keys.query
                # relationship join
                .join(Api_keys.users)
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
                .filter_by(id=id)
                .first_or_404()
            )
        print()
        print('SQL')
        print()
        print()
        print()
        print(data)
        print()
        print()
        print()

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete api_keys')
    @ns.doc(security='jwt')
    # @jwt_required
    def delete(self, id):  # /api_keys/<id>
        '''Delete a Api_keys given its identifier'''
        data = Api_keys.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Api_keys Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update api_keys')
    @ns.expect(api_keys)
    @ns.marshal_list_with(api_keys, code=201)
    @ns.doc(security='jwt')
    # @jwt_required
    def put(self, id):  # /api_keys/<id>
        '''Update a Api_keys given its identifier'''
        data = Api_keys.query.get_or_404(id)
        # start update api_request feilds
        data.api_key = api.payload['api_key']
        data.api_key_notes = api.payload['api_key_notes']
        data.created_user_id = api.payload['created_user_id']
        data.valid_from = fn.convert_to_python_data_type('datetime')(api.payload['valid_from'])
        data.valid_to = fn.convert_to_python_data_type('datetime')(api.payload['valid_to'])
        # end update api_request feilds
        # data.title = api.payload['title']
        db.session.commit()
        return data, 201


# Api_keysList
# shows a list of all Api_keys, and lets you POST to add new Api_keys
@ns.route('/')
class Api_keysListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get api_keys')
    @ns.expect(parser)
    @ns.marshal_list_with(api_keys, code=200)
    @ns.doc(security='jwt')
    # @jwt_required
    def get(self):  # /api_keys
        '''List Api_keys records '''
        args = parser.parse_args()
        page = args['page']

        data = (
                Api_keys.query
                # relationship join
                .join(Api_keys.users)
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
                .items
            )

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert api_keys')
    @ns.expect(api_keys)
    @ns.marshal_with(api_keys, code=201)
    @ns.doc(security='jwt')
    # @jwt_required
    def post(self):  # /api_keys
        '''Create a new Api_keys record'''
        data = Api_keys(
            # start new api_request feilds
            api_key = api.payload['api_key'],
            api_key_notes = api.payload['api_key_notes'],
            created_user_id = api.payload['created_user_id'],
            valid_from = fn.convert_to_python_data_type('datetime')(api.payload['valid_from']),
            valid_to = fn.convert_to_python_data_type('datetime')(api.payload['valid_to'])
            # end new api_request feilds
            # title = api.payload['title']
        )
        db.session.add(data)
        db.session.commit()
        return data, 201


# Api_keysBulk
# Inserts and updates in Bulk of Api_keys, and lets you POST to add and put to update new Api_keys
@ns.route('/bulk')
class Api_keysBulkListResource(Resource):
    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update api_keys')
    @ns.expect(api_keys)
    @ns.marshal_list_with(api_keys, code=201)
    @ns.doc(security='jwt')
    # @jwt_required
    def put(self):  # /api_keys/bulk
        '''Bulk update Api_keys given their identifiers'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_update_mappings(Api_keys,data)
        db.session.commit()
        return data, 201

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert api_keys')
    @ns.expect(api_keys)
    @ns.marshal_with(api_keys, code=201)
    @ns.doc(security='jwt')
    # @jwt_required
    def post(self):  # /api_keys/bulk
        '''Bulk create new Api_keys records'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_insert_mappings(Api_keys,data)
        db.session.commit()
        return data, 201


# Api_keysSeed Data
# Inserts and updates in Bulk of Api_keys, and lets you POST to add and put to update new Api_keys
@ns.route('/seed/<int:level>')
class Api_keysBulkSeedResource(Resource):
    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='seed api_keys')
    # @ns.expect(api_keys)
    # @ns.marshal_with(api_keys, code=201)
    # @ns.doc(security='jwt')
    @ns.doc(security=None)
    # # @jwt_required
    def get(self, level):  # /api_keys/seed/<level>
        '''Seed bulk Api_keys records. Level 1 = `Core` Data, Level 2 = `Nice to Have` Data, Level 3 = `Demo` Data'''
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
        try:
            db.session.bulk_insert_mappings(Api_keys,data)
            db.session.commit()
        
            return data, 201
        except:
            return [{"error":str(sys.exc_info()[0]),"details":str(sys.exc_info()[1])}], 500


# Api_keysAggregate
# shows a list of all Api_keys, and lets you POST to add new Api_keys
@ns.route('/aggregate')
class Api_keysAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get api_keys aggregates')
    @ns.marshal_with(api_keys_agg, code=200)
    @ns.doc(security='jwt')
    # @jwt_required
    def get(self):  # /api_keys
        '''Aggregate Api_keys records '''

        data = Api_keys.query.with_entities(
            
            # start new api_aggregate feilds

                func.count(Api_keys.api_key).label('api_key_count'),

                func.count(Api_keys.api_key_notes).label('api_key_notes_count'),

                func.count(Api_keys.created_user_id).label('created_user_id_count'),

                func.sum(Api_keys.created_user_id).label('created_user_id_sum'),

                func.avg(Api_keys.created_user_id).label('created_user_id_avg'),

                func.min(Api_keys.created_user_id).label('created_user_id_min'),

                func.max(Api_keys.created_user_id).label('created_user_id_max'),
                func.count(Api_keys.valid_from).label('valid_from_count'),

                func.count(Api_keys.valid_to).label('valid_to_count')
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds

                "api_key_count":data.api_key_count,

                "api_key_notes_count":data.api_key_notes_count,

                "created_user_id_count":data.created_user_id_count,

                "created_user_id_sum":data.created_user_id_sum,

                "created_user_id_avg":data.created_user_id_avg,

                "created_user_id_min":data.created_user_id_min,

                "created_user_id_max":data.created_user_id_max,

                "valid_from_count":data.valid_from_count,

                "valid_to_count":data.valid_to_count
            # end new api_aggregate_object feilds
        }

        return data_obj, 200


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Api_keys, "before_insert")
def before_insert(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Api_keys",
            action="Before Insert",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'api_keys', run_type = "before_insert", data = payload, convert_sqlalchemy_to_json = False)

    pass


@event.listens_for(Api_keys, "after_insert")
def after_insert(mapper, connection, target):
    if api.payload:
        payload =str(json.dumps(target.as_dict(), indent=4, default=str))
        
        data = Audit(
            model_name="Api_keys",
            action="After Insert",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'api_keys', run_type = "after_insert", data = payload, convert_sqlalchemy_to_json = False)
    pass


@event.listens_for(Api_keys, "before_update")
def before_update(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Api_keys",
            action="Before Update",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'api_keys', run_type = "before_insert", data = payload, convert_sqlalchemy_to_json = False)
        
    pass


@event.listens_for(Api_keys, "after_update")
def after_update(mapper, connection, target):
    if api.payload:
        payload =str(json.dumps(target.as_dict(), indent=4, default=str))
        
        data = Audit(
            model_name="Api_keys",
            action="After Update",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'api_keys', run_type = "after_update", data = payload, convert_sqlalchemy_to_json = False)
    pass


@event.listens_for(Api_keys, "before_delete")
def before_delete(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Api_keys",
            action="Before Delete",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)

        fn.process_webhook(module_name = 'api_keys', run_type = "before_delete", data = payload, convert_sqlalchemy_to_json = False)
        
    pass


@event.listens_for(Api_keys, "after_delete")
def after_delete(mapper, connection, target):
    pass
