
# Import Flask Resource, fields from flask_restx for API and Swagger
from flask_restx import Resource, fields, reqparse
# Import sql functions (SUM,MIN,MAX,AVG)
from sqlalchemy.sql import func

# JWT for API
from flask_jwt_extended import jwt_required

# Import the database object from the main app module
from app import db, app, api

# Import module models (i.e. User)
from app.mod_api_keys.models import Api_keys

# import json for the bulk operations
import json

# Swagger namespace
ns = api.namespace('api/api_keys', description='Database model "Api_keys", resource based, Api. \
    This API should have 2 endpoints from the name of the model prefixed by "api".')

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
    @jwt_required
    def get(self, id):  # /api_keys/<id>
        '''Fetch a single Api_keys item given its identifier'''
        data = Api_keys.query.get_or_404(id)

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete api_keys')
    @ns.doc(security='jwt')
    @jwt_required
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
    @jwt_required
    def put(self, id):  # /api_keys/<id>
        '''Update a Api_keys given its identifier'''
        data = Api_keys.query.get_or_404(id)
        # start update api_request feilds
        data.api_key = api.payload['api_key']
        data.api_key_notes = api.payload['api_key_notes']
        data.created_user_id = api.payload['created_user_id']
        data.valid_from = api.payload['valid_from']
        data.valid_to = api.payload['valid_to']
        # end update api_request feilds
        # data.title = api.payload['title']
        db.session.commit()
        db.session.refresh(data)
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
    @jwt_required
    def get(self):  # /api_keys
        '''List Api_keys records '''
        args = parser.parse_args()
        page = args['page']

        data = Api_keys.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE']).items

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert api_keys')
    @ns.expect(api_keys)
    @ns.marshal_with(api_keys, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /api_keys
        '''Create a new Api_keys record'''
        data = Api_keys(
            # start new api_request feilds
            api_key=api.payload['api_key'],
            api_key_notes=api.payload['api_key_notes'],
            created_user_id=api.payload['created_user_id'],
            valid_from=api.payload['valid_from'],
            valid_to=api.payload['valid_to']
            # end new api_request feilds
            # title = api.payload['title']
        )
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# Api_keysBulk
# Inserts and updates in Bulk of Api_keys, and lets you POST to add and put to update new Api_keys
@ns.route('/bulk')
class Api_keysListResource(Resource):
    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update api_keys')
    @ns.expect(api_keys)
    @ns.marshal_list_with(api_keys, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self):  # /api_keys/bulk
        '''Bulk update Api_keys given their identifiers'''
        data = json.loads(api.payload)
        db.session.bulk_update_mappings(Api_keys,data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert api_keys')
    @ns.expect(api_keys)
    @ns.marshal_with(api_keys, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /api_keys/bulk
        '''Bulk create new Api_keys records'''
        data = json.loads(api.payload)
        db.session.bulk_insert_mappings(Api_keys,data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# Api_keysAggregate
# shows a list of all Api_keys, and lets you POST to add new Api_keys
@ns.route('/aggregate')
class Api_keysAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get api_keys aggregates')
    @ns.marshal_with(api_keys_agg, code=200)
    @ns.doc(security='jwt')
    @jwt_required
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