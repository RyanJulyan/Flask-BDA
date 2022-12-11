
import secrets

# Import Flask Resource, fields from flask_restx for API and Swagger
from flask_restx import Resource, fields, reqparse
from flask import request

# Import SQLAlchemy Error
from flask_sqlalchemy import SQLAlchemy

# Import the database object from the main app module
from app import db, app, api, jwt, blacklist, bcrypt

# JWT for API
from flask_jwt_extended import get_raw_jwt, jwt_required, create_access_token, \
                                jwt_refresh_token_required, create_refresh_token, \
                                get_jwt_identity, fresh_jwt_required

# Import module models (i.e. Users)
from app.mod_users.models import Users

# Swagger namespace
ns = api.namespace('api/users', description='Database model "Users", resource based, Api. \
    This API should have 5 endpoints from the name of the model prefixed by "api".\
    as well as a login and logout route as well as a refresh token')

user = api.model('Users', {
    'id': fields.Integer(readonly=True, description='The User unique identifier'),
    # start new add_argument
    'name': fields.String(required=True, description='The name of the user'),
    'email': fields.String(required=True, description='The email of the user'),
    'password': fields.String(required=True, description='The password of the user'),
    'role': fields.Integer(required=False, description='The role of the user'),
    'status': fields.Integer(required=False, description='The status of the user')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

user_login = api.model('User_login', {
    'email': fields.String(required=True, description='The email of the user'),
    'password': fields.String(required=True, description='The password of the user'),
    # 'token': fields.String(required=False, description='The password of the user')
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

@ns.route('/login')
class Login(Resource):

    @ns.doc(responses={201: 'LOGGED IN', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='Login user')
    @ns.expect(user_login)
    # @ns.marshal_with(user_login, code=201)
    @ns.doc(security=None)
    def post(self):
        if not request.is_json:
            return {"message": "Missing JSON in request"}, 400

        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if not email:
            return {"message": "Missing email parameter"}, 400
        if not password:
            return {"message": "Missing password parameter"}, 400

        try:
            # user = User.query.filter_by(User.email.like(email)).first()
            user = Users.query.filter_by(email = email).first()
            
            if user and bcrypt.check_password_hash(user.password, password):
                data = user
            else:
                return {"message": "Incorrect username or password"}, 401
        except AttributeError:
            return {"message": "Incorrect username or password"}

        if data is None:
            return {"message": "Incorrect username or password"}, 401

        if data.email is None:
            return {"message": "Incorrect username or password"}, 401

        # Identity can be any data that is json serializable
        ret = {
            'access_token': create_access_token(identity={"email":data.email}),
            'refresh_token': create_refresh_token(identity={"email":data.email})
        }
        return ret, 200


# Refresh token endpoint. This will generate a new access token from
# the refresh token, but will mark that access token as non-fresh,
# as we do not actually verify a password in this endpoint.
@ns.route('/refresh')
class RefreshToken(Resource):

    @ns.doc(responses={201: 'REFRESHED TOKEN', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='Login user')
    @ns.doc(security='jwt')
    @jwt_refresh_token_required
    # @ns.doc(security=None)
    def post(self):
        current_user = get_jwt_identity()
        ret = {
            'access_token': create_access_token(identity=current_user, fresh=False)
        }
        return ret, 200

# # Endpoint for revoking the current users access token
@ns.route('/logout')
class Logout(Resource):

    @ns.doc(responses={201: 'LOGGED OUT', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='Login user')
    @ns.doc(security='jwt')
    # # @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']

        blacklist.add(jti)

        print ({"blacklist": blacklist})

        return {"message": "Successfully logged in using the API"}, 200

@ns.route('/<int:id>')
@ns.response(404, 'User not found')
@ns.param('id', 'The User identifier')
class UserResource(Resource):
    '''Show and edit a single User item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get user')
    @ns.marshal_list_with(user, code=200)
    @ns.doc(security='jwt')
    # @jwt_required
    # @ns.doc(security=None)
    def get(self, id):  # /user/<id>
        '''Fetch a single User item given its identifier'''
        data = Users.query.get_or_404(id)

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete user')
    @ns.doc(security='jwt')
    # @jwt_required
    # @ns.doc(security=None)
    def delete(self, id):  # /user/<id>
        '''Delete a User given its identifier'''
        data = Users.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted User Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update user')
    @ns.expect(user)
    @ns.marshal_list_with(user, code=201)
    @ns.doc(security='jwt')
    # @jwt_required
    # @ns.doc(security=None)
    def put(self, id):  # /user/<id>
        '''Update a User given its identifier'''
        data = Users.query.get_or_404(id)
        # start update api_request feilds
        # this line should be removed and replaced with the updateApiRequestDefinitions variable
        # end update api_request feilds
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# UserList
# shows a list of all User, and lets you POST to add new User
@ns.route('/')
class UserListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get user')
    @ns.expect(parser)
    @ns.marshal_list_with(user, code=200)
    @ns.doc(security='jwt')
    # @jwt_required
    # @ns.doc(security=None)
    def get(self):  # /user
        '''List User records '''
        args = parser.parse_args()
        page = args['page']

        data = Users.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE']).items

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert user')
    @ns.expect(user)
    @ns.marshal_with(user, code=201)
    @ns.doc(security='jwt')
    # @jwt_required
    # @ns.doc(security=None)
    def post(self):  # /user
        """Create a new User record"""
        
        args = parser.parse_args()
        data = Users(
            # start new api_request feilds
            name = request.json.get('name', None),
            email = request.json.get('email', None),
            password = request.json.get('password', None),
            role = request.json.get('role', None),
            status = request.json.get('status', None),
            confirmed = False,
            confirmed_on = None,
            session_token = secrets.token_urlsafe(100)
            # end new api_request feilds
            # title=args['title']
        )
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201
