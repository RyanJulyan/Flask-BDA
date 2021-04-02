
# Import Flask Resource, fields from flask_restx for API and Swagger
from flask_restx import Resource, fields, reqparse
# Import sql functions (SUM,MIN,MAX,AVG)
from sqlalchemy.sql import func

# JWT for API
from flask_jwt_extended import jwt_required

# Import the database object from the main app module
from app import db, app, api

# Import module models (i.e. User)
from app.mod_test.models import Test

# Swagger namespace
ns = api.namespace('api/test', description='Database model "Test", resource based, Api. \
    This API should have 2 endpoints from the name of the model prefixed by "api".')

test = api.model('Test', {
    'id': fields.Integer(readonly=True, description='The Test unique identifier'),
    # start new add_argument
    'name': fields.String(required=True, description='The Test Name')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

test_agg = api.model('Test_agg', {
    # start new add_agg_argument
    'name_count': fields.Integer(readonly=True, description='The Test Name count')    # this line should be removed and replaced with the argumentAggParser variable
    # end new add_agg_argument
    # 'name_count': fields.String(required=True, description='The task count')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from Test into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# Test
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single test item, updates a single test item and lets you delete a test item

@ns.route('/<int:id>')
@ns.response(404, 'Test not found')
@ns.param('id', 'The Test identifier')
class TestResource(Resource):
    '''Show a single Test item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get test')
    @ns.marshal_list_with(test, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self, id):  # /test/<id>
        '''Fetch a single Test item given its identifier'''
        data = Test.query.get_or_404(id)

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete test')
    @ns.doc(security='jwt')
    @jwt_required
    def delete(self, id):  # /test/<id>
        '''Delete a Test given its identifier'''
        data = Test.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Test Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update test')
    @ns.expect(test)
    @ns.marshal_list_with(test, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self, id):  # /test/<id>
        '''Update a Test given its identifier'''
        data = Test.query.get_or_404(id)
        # start update api_request feilds
        data.name = api.payload['name']
        # end update api_request feilds
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# TestList
# shows a list of all Test, and lets you POST to add new Test
@ns.route('/')
class TestListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get test')
    @ns.expect(parser)
    @ns.marshal_list_with(test, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /test
        '''List Test records '''
        args = parser.parse_args()
        page = args['page']

        data = Test.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE']).items

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert test')
    @ns.expect(test)
    @ns.marshal_with(test, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /test
        '''Create a new Test record'''
        args = parser.parse_args()
        data = Test(
            # start new api_request feilds
            name=api.payload['name']
            # end new api_request feilds
            # title=args['title']
        )
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# TestAggregate
# shows a list of all Test, and lets you POST to add new Test
@ns.route('/aggregate')
class TestAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get test aggregates')
    @ns.marshal_with(test_agg, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /test
        '''Aggregate Test records '''

        data = Test.query.with_entities(
            
            # start new api_aggregate feilds

            func.count(Test.name).label('name_count')
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds

            "name_count":data.name_count
            # end new api_aggregate_object feilds
        }

        return data_obj, 200