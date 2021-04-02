
# Import Flask Resource, fields from flask_restx for API and Swagger
from flask_restx import Resource, fields, reqparse
# Import sql functions (SUM,MIN,MAX,AVG)
from sqlalchemy.sql import func

# JWT for API
from flask_jwt_extended import jwt_required

# Import the database object from the main app module
from app import db, app, api

# Import module models (i.e. User)
from app.mod_hierarchies.models import Hierarchies

# Swagger namespace
ns = api.namespace('api/hierarchies', description='Database model "Hierarchies", resource based, Api. \
    This API should have 2 endpoints from the name of the model prefixed by "api".')

hierarchies = api.model('Hierarchies', {
    'id': fields.Integer(readonly=True, description='The Hierarchies unique identifier'),
    # start new add_argument
    'organisation_id': fields.Float(required=True, description='The Hierarchies Organisation id'),
    'name': fields.String(required=True, description='The Hierarchies Name'),
    'path': fields.String(required=True, description='The Hierarchies Path'),
    'rank': fields.Float(description='The Hierarchies Rank'),
    'parent_id': fields.Float(description='The Hierarchies Parent id'),
    'key_value': fields.String(description='The Hierarchies Key value')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

hierarchies_agg = api.model('Hierarchies_agg', {
    # start new add_agg_argument
    'organisation_id_count': fields.Integer(readonly=True, description='The Hierarchies Organisation id count'),
    'organisation_id_sum': fields.Float(readonly=True, description='The Hierarchies Organisation id sum'),
    'organisation_id_avg': fields.Float(readonly=True, description='The Hierarchies Organisation id avg'),
    'organisation_id_min': fields.Float(readonly=True, description='The Hierarchies Organisation id min'),
    'organisation_id_max': fields.Float(readonly=True, description='The Hierarchies Organisation id max'),
    'name_count': fields.Integer(readonly=True, description='The Hierarchies Name count'),
    'path_count': fields.Integer(readonly=True, description='The Hierarchies Path count'),
    'rank_count': fields.Integer(readonly=True, description='The Hierarchies Rank count'),
    'rank_sum': fields.Float(readonly=True, description='The Hierarchies Rank sum'),
    'rank_avg': fields.Float(readonly=True, description='The Hierarchies Rank avg'),
    'rank_min': fields.Float(readonly=True, description='The Hierarchies Rank min'),
    'rank_max': fields.Float(readonly=True, description='The Hierarchies Rank max'),
    'parent_id_count': fields.Integer(readonly=True, description='The Hierarchies Parent id count'),
    'parent_id_sum': fields.Float(readonly=True, description='The Hierarchies Parent id sum'),
    'parent_id_avg': fields.Float(readonly=True, description='The Hierarchies Parent id avg'),
    'parent_id_min': fields.Float(readonly=True, description='The Hierarchies Parent id min'),
    'parent_id_max': fields.Float(readonly=True, description='The Hierarchies Parent id max'),
    'key_value_count': fields.Integer(readonly=True, description='The Hierarchies Key value count')    # this line should be removed and replaced with the argumentAggParser variable
    # end new add_agg_argument
    # 'name_count': fields.String(required=True, description='The task count')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from Hierarchies into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# Hierarchies
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single hierarchies item, updates a single hierarchies item and lets you delete a hierarchies item

@ns.route('/<int:id>')
@ns.response(404, 'Hierarchies not found')
@ns.param('id', 'The Hierarchies identifier')
class HierarchiesResource(Resource):
    '''Show a single Hierarchies item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get hierarchies')
    @ns.marshal_list_with(hierarchies, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self, id):  # /hierarchies/<id>
        '''Fetch a single Hierarchies item given its identifier'''
        data = Hierarchies.query.get_or_404(id)

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete hierarchies')
    @ns.doc(security='jwt')
    @jwt_required
    def delete(self, id):  # /hierarchies/<id>
        '''Delete a Hierarchies given its identifier'''
        data = Hierarchies.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Hierarchies Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update hierarchies')
    @ns.expect(hierarchies)
    @ns.marshal_list_with(hierarchies, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self, id):  # /hierarchies/<id>
        '''Update a Hierarchies given its identifier'''
        data = Hierarchies.query.get_or_404(id)
        # start update api_request feilds
        data.organisation_id = api.payload['organisation_id']
        data.name = api.payload['name']
        data.path = api.payload['path']
        data.rank = api.payload['rank']
        data.parent_id = api.payload['parent_id']
        data.key_value = api.payload['key_value']
        # end update api_request feilds
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# HierarchiesList
# shows a list of all Hierarchies, and lets you POST to add new Hierarchies
@ns.route('/')
class HierarchiesListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get hierarchies')
    @ns.expect(parser)
    @ns.marshal_list_with(hierarchies, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /hierarchies
        '''List Hierarchies records '''
        args = parser.parse_args()
        page = args['page']

        data = Hierarchies.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE']).items

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert hierarchies')
    @ns.expect(hierarchies)
    @ns.marshal_with(hierarchies, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /hierarchies
        '''Create a new Hierarchies record'''
        args = parser.parse_args()
        data = Hierarchies(
            # start new api_request feilds
            organisation_id=api.payload['organisation_id'],
            name=api.payload['name'],
            path=api.payload['path'],
            rank=api.payload['rank'],
            parent_id=api.payload['parent_id'],
            key_value=api.payload['key_value']
            # end new api_request feilds
            # title=args['title']
        )
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
        return data, 201


# HierarchiesAggregate
# shows a list of all Hierarchies, and lets you POST to add new Hierarchies
@ns.route('/aggregate')
class HierarchiesAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get hierarchies aggregates')
    @ns.marshal_with(hierarchies_agg, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /hierarchies
        '''Aggregate Hierarchies records '''

        data = Hierarchies.query.with_entities(
            
            # start new api_aggregate feilds

            func.count(Hierarchies.organisation_id).label('organisation_id_count'),

            func.sum(Hierarchies.organisation_id).label('organisation_id_sum'),

            func.avg(Hierarchies.organisation_id).label('organisation_id_avg'),

            func.min(Hierarchies.organisation_id).label('organisation_id_min'),

            func.max(Hierarchies.organisation_id).label('organisation_id_max')
            func.count(Hierarchies.name).label('name_count'),

            func.count(Hierarchies.path).label('path_count'),

            func.count(Hierarchies.rank).label('rank_count'),

            func.sum(Hierarchies.rank).label('rank_sum'),

            func.avg(Hierarchies.rank).label('rank_avg'),

            func.min(Hierarchies.rank).label('rank_min'),

            func.max(Hierarchies.rank).label('rank_max')
            func.count(Hierarchies.parent_id).label('parent_id_count'),

            func.sum(Hierarchies.parent_id).label('parent_id_sum'),

            func.avg(Hierarchies.parent_id).label('parent_id_avg'),

            func.min(Hierarchies.parent_id).label('parent_id_min'),

            func.max(Hierarchies.parent_id).label('parent_id_max')
            func.count(Hierarchies.key_value).label('key_value_count')
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds

            "organisation_id_count":data.organisation_id_count,

            "organisation_id_sum":data.organisation_id_sum,

            "organisation_id_avg":data.organisation_id_avg,

            "organisation_id_min":data.organisation_id_min,

            "organisation_id_max":data.organisation_id_max,

            "name_count":data.name_count,

            "path_count":data.path_count,

            "rank_count":data.rank_count,

            "rank_sum":data.rank_sum,

            "rank_avg":data.rank_avg,

            "rank_min":data.rank_min,

            "rank_max":data.rank_max,

            "parent_id_count":data.parent_id_count,

            "parent_id_sum":data.parent_id_sum,

            "parent_id_avg":data.parent_id_avg,

            "parent_id_min":data.parent_id_min,

            "parent_id_max":data.parent_id_max,

            "key_value_count":data.key_value_count
            # end new api_aggregate_object feilds
        }

        return data_obj, 200