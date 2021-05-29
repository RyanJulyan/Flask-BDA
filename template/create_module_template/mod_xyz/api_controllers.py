
# Import Flask Resource, fields from flask_restx for API and Swagger
from flask_restx import Resource, fields, reqparse
# Import sql functions (SUM,MIN,MAX,AVG)
from sqlalchemy.sql import func

# JWT for API
from flask_jwt_extended import jwt_required

# Import the database object from the main app module
from app import db, app, api

# Import module models (i.e. User)
from app.mod_xyz.models import Xyz

# Import json for consuming payload and for payload data type transformations
import json

# Import read_json from pandas for payload data type transformations
from pandas import read_json

# Swagger namespace
ns = api.namespace('api/xyz', description='Database model "Xyz", resource based, Api. \
    This API should have 2 endpoints from the name of the model prefixed by "api".')

xyz = api.model('Xyz', {
    'id': fields.Integer(readonly=True, description='The Xyz unique identifier'),
    # start new add_argument
    # this line should be removed and replaced with the argumentParser variable
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

xyz_agg = api.model('Xyz_agg', {
    # start new add_agg_argument
    # this line should be removed and replaced with the argumentAggParser variable
    # end new add_agg_argument
    # 'name_count': fields.String(required=True, description='The task count')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from Xyz into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# Xyz
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single xyz item, updates a single xyz item and lets you delete a xyz item

@ns.route('/<int:id>')
@ns.response(404, 'Xyz not found')
@ns.param('id', 'The Xyz identifier')
class XyzResource(Resource):
    '''Show a single Xyz item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get xyz')
    @ns.marshal_list_with(xyz, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self, id):  # /xyz/<id>
        '''Fetch a single Xyz item given its identifier'''
        data = Xyz.query.get_or_404(id)

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete xyz')
    @ns.doc(security='jwt')
    @jwt_required
    def delete(self, id):  # /xyz/<id>
        '''Delete a Xyz given its identifier'''
        data = Xyz.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Xyz Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update xyz')
    @ns.expect(xyz)
    @ns.marshal_list_with(xyz, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self, id):  # /xyz/<id>
        '''Update a Xyz given its identifier'''
        data = Xyz.query.get_or_404(id)
        # start update api_request feilds
        # this line should be removed and replaced with the updateApiRequestDefinitions variable
        # end update api_request feilds
        # data.title = api.payload['title']
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# XyzList
# shows a list of all Xyz, and lets you POST to add new Xyz
@ns.route('/')
class XyzListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get xyz')
    @ns.expect(parser)
    @ns.marshal_list_with(xyz, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /xyz
        '''List Xyz records '''
        args = parser.parse_args()
        page = args['page']

        data = Xyz.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE']).items

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert xyz')
    @ns.expect(xyz)
    @ns.marshal_with(xyz, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /xyz
        '''Create a new Xyz record'''
        data = Xyz(
            # start new api_request feilds
            # this line should be removed and replaced with the newApiRequestDefinitions variable
            # end new api_request feilds
            # title = api.payload['title']
        )
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# XyzBulk
# Inserts and updates in Bulk of Xyz, and lets you POST to add and put to update new Xyz
@ns.route('/bulk')
class XyzListResource(Resource):
    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update xyz')
    @ns.expect(xyz)
    @ns.marshal_list_with(xyz, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self):  # /xyz/bulk
        '''Bulk update Xyz given their identifiers'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_update_mappings(Xyz,data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert xyz')
    @ns.expect(xyz)
    @ns.marshal_with(xyz, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /xyz/bulk
        '''Bulk create new Xyz records'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_insert_mappings(Xyz,data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# XyzAggregate
# shows a list of all Xyz, and lets you POST to add new Xyz
@ns.route('/aggregate')
class XyzAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get xyz aggregates')
    @ns.marshal_with(xyz_agg, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /xyz
        '''Aggregate Xyz records '''

        data = Xyz.query.with_entities(
            
            # start new api_aggregate feilds
            # this line should be removed and replaced with the newApiAggregateDefinitions variable
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds
            # this line should be removed and replaced with the newApiAggregateObjectDefinitions variable
            # end new api_aggregate_object feilds
        }

        return data_obj, 200