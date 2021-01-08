
# Import Flask Restful for API
from flask_restful import reqparse, abort, Resource

# Import the database object from the main app module
from app import db

# Import module forms
# from app.mod_xyz.forms import LoginForm

# Import module models (i.e. User)
from app.mod_xyz.models import Xyz


def abort_if_doesnt_exist(id, data):
    if id not in data:
        abort(404, message="Xyz {} doesn't exist".format(id))


parser = reqparse.RequestParser()
# start new add_argument
# this line should be removed and replaced with the argument variable
# end new add_argument

# parser.add_argument('example')

# Xyz
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# shows a single xyz item, updates a single xyz item and lets you delete a xyz item


class XyzResource(Resource):
    def get(self, id):  # /xyz/<id>
        abort_if_doesnt_exist(id)
        return TODOS[id]

    def delete(self, id):  # /xyz/<id>
        abort_if_doesnt_exist(id)
        del TODOS[id]
        return '', 204

    def put(self, id):  # /xyz/<id>
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[id] = task
        return task, 201


# XyzList
# shows a list of all Xyz, and lets you POST to add new Xyz
class XyzListResource(Resource):
    def get(self):  # /xyz
        return TODOS

    def post(self):  # /xyz
        args = parser.parse_args()
        id = int(max(TODOS.keys()).lstrip('todo')) + 1
        TODOS[id] = {'task': args['task']}
        return TODOS[id], 201
