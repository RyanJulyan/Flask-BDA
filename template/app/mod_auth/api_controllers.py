
# Import Flask Resource, fields from flask_restx for API and Swagger
from flask_restx import Resource, fields, reqparse
from flask import request, jsonify

# Import the database object from the main app module
from app import db, app, api, blacklist

# JWT for API
from flask_jwt_extended import get_raw_jwt, jwt_required, create_access_token, \
                                jwt_refresh_token_required, create_refresh_token, \
                                get_jwt_identity, fresh_jwt_required

# Import module models (i.e. User)
from app.mod_auth.models import User

# Swagger namespace
ns = api.namespace('api/auth', description='Database model "User", resource based, Api. \
    This API should have 5 endpoints from the name of the model prefixed by "api".\
    as well as a login and logout route as well as a refresh token')

user = api.model('User', {
    'id': fields.Integer(readonly=True, description='The User unique identifier'),
    # start new add_argument
    'name': fields.String(required=True, description='The name of the user'),
    'email': fields.String(required=True, description='The email of the user'),
    'password': fields.String(required=True, description='The password of the user'),
    'role': fields.SmallInteger(required=False, description='The role of the user'),
    'status': fields.SmallInteger(required=False, description='The status of the user')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from User into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# User
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single user item, updates a single user item and lets you delete a user item

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@ns.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    data = User.query.filter(User.email == email, User.password == password)

    if data is not None:
        return jsonify({"msg": "Incorrect username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=data.email)
    return jsonify(access_token=access_token), 200

# Refresh token endpoint. This will generate a new access token from
# the refresh token, but will mark that access token as non-fresh,
# as we do not actually verify a password in this endpoint.
@ns.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    ret = {'access_token': new_token}
    return jsonify(ret), 200

# Endpoint for revoking the current users access token
@ns.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

@ns.route('/<int:id>')
@ns.response(404, 'User not found')
@ns.param('id', 'The User identifier')
@jwt_required
class XyzResource(Resource):
    '''Show a single User item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get user')
    @ns.marshal_list_with(user, code=200)
    def get(self, id):  # /user/<id>
        '''Fetch a single User item given its identifier'''
        data = User.query.get(id)

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete user')
    def delete(self, id):  # /user/<id>
        '''Delete a User given its identifier'''
        data = User.query.get(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted User Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update user')
    @ns.expect(user)
    @ns.marshal_list_with(user, code=201)
    def put(self, id):  # /user/<id>
        '''Update a User given its identifier'''
        data = User.query.get(id)
        # start update api_request feilds
        # this line should be removed and replaced with the updateApiRequestDefinitions variable
        # end update api_request feilds
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# UserList
# shows a list of all User, and lets you POST to add new User
@ns.route('/')
@jwt_required
class XyzListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get user')
    @ns.expect(parser)
    @ns.marshal_list_with(user, code=200)
    def get(self):  # /user
        '''List User records '''
        args = parser.parse_args()
        page = args['page']

        data = User.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE']).items

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert user')
    @ns.expect(user)
    @ns.marshal_with(user, code=201)
    def post(self):  # /user
        """Create a new User record"""
        args = parser.parse_args()
        data = User(
            # start new api_request feilds
            name=args['name'],
            email=args['email'],
            password=args['name'],
            status=args['status']
            # end new api_request feilds
            # title=args['title']
        )
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201
