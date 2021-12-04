
# Import Flask Resource, fields from flask_restx for API and Swagger
from flask_restx import Resource, fields, reqparse
# Import sql functions (SUM,MIN,MAX,AVG)
from sqlalchemy.sql import func
# Import sql events 
from sqlalchemy import event

# JWT for API
from flask_jwt_extended import jwt_required

# Import the database object from the main app module
from app import db, app, api

# Import helper functions, comment in as needed (commented out for performance)
# from app.mod_helper_functions import functions as fn

# Import module models (i.e. User)
from app.mod_site_settings.models import Site_settings

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
ns = api.namespace('api/site_settings', description='Database model "Site_settings", resource based, Api. \
    This API should have 2 endpoints from the name of the model prefixed by "api".')

site_settings = api.model('Site_settings', {
    'id': fields.Integer(readonly=True, description='The Site_settings unique identifier'),
    # start new add_argument
    'organisation_id': fields.Float(required=True, description='The Site_settings Organisation id'),
    'key': fields.String(required=True, description='The Site_settings Key'),
    'display_name': fields.String(required=True, description='The Site_settings Display name'),
    'description': fields.String(required=True, description='The Site_settings Description'),
    'value': fields.String(description='The Site_settings Value'),
    'data_type': fields.String(required=True, description='The Site_settings Data type'),
    'group': fields.String(required=True, description='The Site_settings Group'),
    'key_value': fields.String(description='The Site_settings Key value')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

site_settings_agg = api.model('Site_settings_agg', {
    # start new add_agg_argument
    'organisation_id_count': fields.Integer(readonly=True, description='The Site_settings Organisation id count'),
    'organisation_id_sum': fields.Float(readonly=True, description='The Site_settings Organisation id sum'),
    'organisation_id_avg': fields.Float(readonly=True, description='The Site_settings Organisation id avg'),
    'organisation_id_min': fields.Float(readonly=True, description='The Site_settings Organisation id min'),
    'organisation_id_max': fields.Float(readonly=True, description='The Site_settings Organisation id max'),
    'key_count': fields.Integer(readonly=True, description='The Site_settings Key count'),
    'display_name_count': fields.Integer(readonly=True, description='The Site_settings Display name count'),
    'description_count': fields.Integer(readonly=True, description='The Site_settings Description count'),
    'value_count': fields.Integer(readonly=True, description='The Site_settings Value count'),
    'data_type_count': fields.Integer(readonly=True, description='The Site_settings Data type count'),
    'group_count': fields.Integer(readonly=True, description='The Site_settings Group count'),
    'key_value_count': fields.Integer(readonly=True, description='The Site_settings Key value count')    # this line should be removed and replaced with the argumentAggParser variable
    # end new add_agg_argument
    # 'name_count': fields.String(required=True, description='The task count')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from Site_settings into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# Site_settings
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single site_settings item, updates a single site_settings item and lets you delete a site_settings item

@ns.route('/<int:id>')
@ns.response(404, 'Site_settings not found')
@ns.param('id', 'The Site_settings identifier')
class Site_settingsResource(Resource):
    '''Show a single Site_settings item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get site_settings')
    @ns.marshal_list_with(site_settings, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self, id):  # /site_settings/<id>
        '''Fetch a single Site_settings item given its identifier'''
        data = Site_settings.query.get_or_404(id)

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete site_settings')
    @ns.doc(security='jwt')
    @jwt_required
    def delete(self, id):  # /site_settings/<id>
        '''Delete a Site_settings given its identifier'''
        data = Site_settings.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Site_settings Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update site_settings')
    @ns.expect(site_settings)
    @ns.marshal_list_with(site_settings, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self, id):  # /site_settings/<id>
        '''Update a Site_settings given its identifier'''
        data = Site_settings.query.get_or_404(id)
        # start update api_request feilds
        data.organisation_id = api.payload['organisation_id']
        data.key = api.payload['key']
        data.display_name = api.payload['display_name']
        data.description = api.payload['description']
        data.value = api.payload['value']
        data.data_type = api.payload['data_type']
        data.group = api.payload['group']
        data.key_value = api.payload['key_value']
        # end update api_request feilds
        # data.title = api.payload['title']
        db.session.commit()
        return data, 201


# Site_settingsList
# shows a list of all Site_settings, and lets you POST to add new Site_settings
@ns.route('/')
class Site_settingsListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get site_settings')
    @ns.expect(parser)
    @ns.marshal_list_with(site_settings, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /site_settings
        '''List Site_settings records '''
        args = parser.parse_args()
        page = args['page']

        data = Site_settings.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE']).items

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert site_settings')
    @ns.expect(site_settings)
    @ns.marshal_with(site_settings, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /site_settings
        '''Create a new Site_settings record'''
        data = Site_settings(
            # start new api_request feilds
            organisation_id=api.payload['organisation_id'],
            key=api.payload['key'],
            display_name=api.payload['display_name'],
            description=api.payload['description'],
            value=api.payload['value'],
            data_type=api.payload['data_type'],
            group=api.payload['group'],
            key_value=api.payload['key_value']
            # end new api_request feilds
            # title = api.payload['title']
        )
        db.session.add(data)
        db.session.commit()
        return data, 201


# Site_settingsBulk
# Inserts and updates in Bulk of Site_settings, and lets you POST to add and put to update new Site_settings
@ns.route('/bulk')
class Site_settingsBulkListResource(Resource):
    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update site_settings')
    @ns.expect(site_settings)
    @ns.marshal_list_with(site_settings, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self):  # /site_settings/bulk
        '''Bulk update Site_settings given their identifiers'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_update_mappings(Site_settings,data)
        db.session.commit()
        return data, 201

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert site_settings')
    @ns.expect(site_settings)
    @ns.marshal_with(site_settings, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /site_settings/bulk
        '''Bulk create new Site_settings records'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_insert_mappings(Site_settings,data)
        db.session.commit()
        return data, 201


# Site_settingsSeed Data
# Inserts and updates in Bulk of Site_settings, and lets you POST to add and put to update new Site_settings
@ns.route('/seed/<int:level>')
class Site_settingsBulkListResource(Resource):
    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='seed site_settings')
    @ns.expect(site_settings)
    @ns.marshal_with(site_settings, code=201)
    # @ns.doc(security='jwt')
    @ns.doc(security=None)
    # @jwt_required
    def get(self, level):  # /site_settings/seed/<level>
        '''Seed bulk Site_settings records. Level 1 = `Core` Data, Level 2 = `Nice to Have` Data, Level 3 = `Demo` Data'''
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
        db.session.bulk_insert_mappings(Site_settings,data)
        db.session.commit()
        return data, 201


# Site_settingsAggregate
# shows a list of all Site_settings, and lets you POST to add new Site_settings
@ns.route('/aggregate')
class Site_settingsAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get site_settings aggregates')
    @ns.marshal_with(site_settings_agg, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /site_settings
        '''Aggregate Site_settings records '''

        data = Site_settings.query.with_entities(
            
            # start new api_aggregate feilds

                func.count(Site_settings.organisation_id).label('organisation_id_count'),

                func.sum(Site_settings.organisation_id).label('organisation_id_sum'),

                func.avg(Site_settings.organisation_id).label('organisation_id_avg'),

                func.min(Site_settings.organisation_id).label('organisation_id_min'),

                func.max(Site_settings.organisation_id).label('organisation_id_max'),
                func.count(Site_settings.key).label('key_count'),

                func.count(Site_settings.display_name).label('display_name_count'),

                func.count(Site_settings.description).label('description_count'),

                func.count(Site_settings.value).label('value_count'),

                func.count(Site_settings.data_type).label('data_type_count'),

                func.count(Site_settings.group).label('group_count'),

                func.count(Site_settings.key_value).label('key_value_count')
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds

                "organisation_id_count":data.organisation_id_count,

                "organisation_id_sum":data.organisation_id_sum,

                "organisation_id_avg":data.organisation_id_avg,

                "organisation_id_min":data.organisation_id_min,

                "organisation_id_max":data.organisation_id_max,

                "key_count":data.key_count,

                "display_name_count":data.display_name_count,

                "description_count":data.description_count,

                "value_count":data.value_count,

                "data_type_count":data.data_type_count,

                "group_count":data.group_count,

                "key_value_count":data.key_value_count
            # end new api_aggregate_object feilds
        }

        return data_obj, 200


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Site_settings, "before_insert")
def before_insert(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Site_settings",
        action="Before Insert",
        context="Rest API",
        payload=payload
    )
    db.session.add(data)
    db.session.commit()
    pass


@event.listens_for(Site_settings, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Site_settings, "before_update")
def before_update(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Site_settings",
        action="Before Update",
        context="Rest API",
        payload=payload
    )
    db.session.add(data)
    db.session.commit()
    pass


@event.listens_for(Site_settings, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Site_settings, "before_delete")
def before_delete(mapper, connection, target):
    pass


@event.listens_for(Site_settings, "after_delete")
def after_delete(mapper, connection, target):
    pass
