
# Import Flask Restful for API
from flask_restful import reqparse, abort

# Import Flask Resource from Swagger for API
from flask_restful_swagger_3 import swagger, Resource

# Import the database object from the main app module
from app import db, app

# Import module models (i.e. User)
from app.mod_xyz.models import Xyz


def abort_if_doesnt_exist(id, data):
    if id not in data:
        abort(404, message="Xyz {} doesn't exist".format(id))


parser = reqparse.RequestParser()
# start new add_argument
# this line should be removed and replaced with the argumentParser variable
# end new add_argument
parser.add_argument('page')
# parser.add_argument('example')

# Xyz
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# shows a single xyz item, updates a single xyz item and lets you delete a xyz item


class XyzResource(Resource):
    @swagger.tags(['xyz'])
    @swagger.response(response_code=201, description='get xyz')
    def get(self, id):  # /xyz/<id>
        data = Xyz.query.get(id)

        abort_if_doesnt_exist(id, data)
        return data

    @swagger.tags(['xyz'])
    @swagger.response(response_code=204, description='delete xyz')
    def delete(self, id):  # /xyz/<id>
        data = Xyz.query.get(id)

        abort_if_doesnt_exist(id, data)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Xyz Record', 204

    @swagger.tags(['xyz'])
    @swagger.response(response_code=201, description='update xyz')
    @swagger.reqparser(name='XyzModel', parser=parser)
    def put(self, id):  # /xyz/<id>
        args = parser.parse_args()
        data = Xyz.query.get(id)
        # start update api_request feilds
        # this line should be removed and replaced with the updateApiRequestDefinitions variable
        # end update api_request feilds
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# XyzList
# shows a list of all Xyz, and lets you POST to add new Xyz
class XyzListResource(Resource):
    @swagger.tags(['xyz'])
    @swagger.response(response_code=201, description='get xyz')
    def get(self):  # /xyz
        args = parser.parse_args()
        page = args['page']

        data = Xyz.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])

        abort_if_doesnt_exist(id, data)
        return data

    @swagger.tags(['xyz'])
    @swagger.response(response_code=201, description='get xyz')
    @swagger.reqparser(name='XyzModel', parser=parser)
    def post(self):  # /xyz
        args = parser.parse_args()
        data = Xyz(
            # start new api_request feilds
            # this line should be removed and replaced with the newApiRequestDefinitions variable
            # end new api_request feilds
            # title=args['title']
        )
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201
