
# Import Flask Restful for API
from flask_restful import reqparse, abort

# Import Flask Resource from Swagger for API
from flask_restful_swagger_3 import swagger, Resource

# Import the database object from the main app module
from app import db, app

# Import module models (i.e. User)
from app.mod_test.models import Test


def abort_if_doesnt_exist(id, data):
    if id not in data:
        abort(404, message="Test {} doesn't exist".format(id))


parser = reqparse.RequestParser()
# start new add_argument
parser.add_argument('name', required=True, help='name of Name')
# end new add_argument
parser.add_argument('page')
# parser.add_argument('example')

# Test
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# shows a single test item, updates a single test item and lets you delete a test item


class TestResource(Resource):
    @swagger.tags(['test'])
    @swagger.response(response_code=201, description='get test')
    def get(self, id):  # /test/<id>
        data = Test.query.get(id)

        abort_if_doesnt_exist(id, data)
        return data

    @swagger.tags(['test'])
    @swagger.response(response_code=204, description='delete test')
    def delete(self, id):  # /test/<id>
        data = Test.query.get(id)

        abort_if_doesnt_exist(id, data)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Test Record', 204

    @swagger.tags(['test'])
    @swagger.response(response_code=201, description='update test')
    @swagger.reqparser(name='TestModel', parser=parser)
    def put(self, id):  # /test/<id>
        args = parser.parse_args()
        data = Test.query.get(id)
        # start update api_request feilds

        # end update api_request feilds
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# TestList
# shows a list of all Test, and lets you POST to add new Test
class TestListResource(Resource):
    @swagger.tags(['test'])
    @swagger.response(response_code=201, description='get test')
    def get(self):  # /test
        args = parser.parse_args()
        page = args['page']

        data = Test.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

        abort_if_doesnt_exist(id, data)
        return data

    @swagger.tags(['test'])
    @swagger.response(response_code=201, description='get test')
    @swagger.reqparser(name='TestModel', parser=parser)
    def post(self):  # /test
        args = parser.parse_args()
        data = Test(
            # start new api_request feilds

            # end new api_request feilds
            # title=args['title']
        )
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201
