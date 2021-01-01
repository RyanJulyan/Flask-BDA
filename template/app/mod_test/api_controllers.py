
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import Flask Restful for API
from flask_restful import reqparse, abort, Resource

# Import the database object from the main app module
from app import db

# Import module forms
# from app.mod_test.forms import LoginForm

# Import module models (i.e. User)
from app.mod_test.models import Test

def abort_if_doesnt_exist(id,data):
    if id not in data:
        abort(404, message="Test {} doesn't exist".format(id))

parser = reqparse.RequestParser()
# start new add_argument
# this line should be removed and replaced with the argument variable
# end new add_argument

# parser.add_argument('example')

# Test
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# shows a single test item, updates a single test item and lets you delete a test item
class TestResource(Resource):
    def get(self, id): # /test/<id>
        abort_if_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, id): # /test/<id>
        abort_if_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, id): # /test/<id>
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TestList
# shows a list of all Test, and lets you POST to add new Test
class TestListResource(Resource):
    def get(self): # /test
        return TODOS

    def post(self): # /test
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201