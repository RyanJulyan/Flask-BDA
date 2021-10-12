
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

# Import test module models 
from app.mod_test.models import Test
# Import module models (e.g. User)
from app.mod_users.models import Users

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
ns = api.namespace('api/test', description='Database model "Test", resource based, Api. \
    This API should have 9 endpoints from the name of the model prefixed by "api".\
    There are standard 5 CRUD APIs, a 2 BULK APIs, 1 Seed, and 1 Aggregate')

test = api.model('Test', {
    'id': fields.Integer(readonly=True, description='The Test unique identifier'),
    # start new add_argument
    'budget': fields.Float(required=True, description='The Test Budget'),
    'name': fields.String(required=True, description='The Test Name'),
    'test_id': fields.Float(required=True, description='The Test Test id')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

test_agg = api.model('Test_agg', {
    # start new add_agg_argument
    'budget_count': fields.Integer(readonly=True, description='The Test Budget count'),
    'budget_sum': fields.Float(readonly=True, description='The Test Budget sum'),
    'budget_avg': fields.Float(readonly=True, description='The Test Budget avg'),
    'budget_min': fields.Float(readonly=True, description='The Test Budget min'),
    'budget_max': fields.Float(readonly=True, description='The Test Budget max'),
    'name_count': fields.Integer(readonly=True, description='The Test Name count'),
    'test_id_count': fields.Integer(readonly=True, description='The Test Test id count'),
    'test_id_sum': fields.Float(readonly=True, description='The Test Test id sum'),
    'test_id_avg': fields.Float(readonly=True, description='The Test Test id avg'),
    'test_id_min': fields.Float(readonly=True, description='The Test Test id min'),
    'test_id_max': fields.Float(readonly=True, description='The Test Test id max')    # this line should be removed and replaced with the argumentAggParser variable
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
        data = (
                Test.query
                # relationship join
                .join(Users)
                .get_or_404(id)
            )

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
        data.budget = api.payload['budget']
        data.name = api.payload['name']
        data.test_id = api.payload['test_id']
        # end update api_request feilds
        # data.title = api.payload['title']
        db.session.commit()
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

        data = (
                Test.query
                # relationship join
                .join(Users)
                .paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])
                .items
            )

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert test')
    @ns.expect(test)
    @ns.marshal_with(test, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /test
        '''Create a new Test record'''
        data = Test(
            # start new api_request feilds
            budget=api.payload['budget'],
            name=api.payload['name'],
            test_id=api.payload['test_id']
            # end new api_request feilds
            # title = api.payload['title']
        )
        db.session.add(data)
        db.session.commit()
        return data, 201


# TestBulk
# Inserts and updates in Bulk of Test, and lets you POST to add and put to update new Test
@ns.route('/bulk')
class TestBulkListResource(Resource):
    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update test')
    @ns.expect(test)
    @ns.marshal_list_with(test, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self):  # /test/bulk
        '''Bulk update Test given their identifiers'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_update_mappings(Test,data)
        db.session.commit()
        return data, 201

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert test')
    @ns.expect(test)
    @ns.marshal_with(test, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /test/bulk
        '''Bulk create new Test records'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_insert_mappings(Test,data)
        db.session.commit()
        return data, 201


# TestSeed Data
# Inserts and updates in Bulk of Test, and lets you POST to add and put to update new Test
@ns.route('/seed/<int:level>')
class TestBulkSeedResource(Resource):
    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='seed test')
    # @ns.expect(test)
    # @ns.marshal_with(test, code=201)
    # @ns.doc(security='jwt')
    @ns.doc(security=None)
    # @jwt_required
    def post(self, level):  # /test/seed/<level>
        '''Seed bulk Test records. Level 1 = `Core` Data, Level 2 = `Nice to Have` Data, Level 3 = `Demo` Data'''
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
        db.session.bulk_insert_mappings(Test,data)
        db.session.commit()
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

                func.count(Test.budget).label('budget_count'),

                func.sum(Test.budget).label('budget_sum'),

                func.avg(Test.budget).label('budget_avg'),

                func.min(Test.budget).label('budget_min'),

                func.max(Test.budget).label('budget_max'),
                func.count(Test.name).label('name_count'),

                func.count(Test.test_id).label('test_id_count'),

                func.sum(Test.test_id).label('test_id_sum'),

                func.avg(Test.test_id).label('test_id_avg'),

                func.min(Test.test_id).label('test_id_min'),

                func.max(Test.test_id).label('test_id_max')
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds

                "budget_count":data.budget_count,

                "budget_sum":data.budget_sum,

                "budget_avg":data.budget_avg,

                "budget_min":data.budget_min,

                "budget_max":data.budget_max,

                "name_count":data.name_count,

                "test_id_count":data.test_id_count,

                "test_id_sum":data.test_id_sum,

                "test_id_avg":data.test_id_avg,

                "test_id_min":data.test_id_min,

                "test_id_max":data.test_id_max
            # end new api_aggregate_object feilds
        }

        return data_obj, 200


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Test, "before_insert")
def before_insert(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Test",
            action="Before Insert",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Test, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Test, "before_update")
def before_update(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Test",
            action="Before Update",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Test, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Test, "before_delete")
def before_delete(mapper, connection, target):
    if api.payload:
        payload = json.dumps(api.payload)
        
        data = Audit(
            model_name="Test",
            action="Before Delete",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Test, "after_delete")
def after_delete(mapper, connection, target):
    pass
