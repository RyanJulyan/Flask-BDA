
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
# from app.mod_helper_functions import functions as fn

# Import module models (i.e. User)
from app.mod_calendar_definitions.models import Calendar_definitions

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
ns = api.namespace('api/calendar_definitions', description='Database model "Calendar_definitions", resource based, Api. \
    This API should have 9 endpoints from the name of the model prefixed by "api".\
    There are standard 5 CRUD APIs, a 2 BULK APIs, 1 Seed, and 1 Aggregate')

calendar_definitions = api.model('Calendar_definitions', {
    'id': fields.Integer(readonly=True, description='The Calendar_definitions unique identifier'),
    # start new add_argument
    'name': fields.String(required=True, description='The Calendar_definitions Name'),
    'start': fields.String(description='The Calendar_definitions Start'),
    'end': fields.String(description='The Calendar_definitions End'),
    'range_history_periods': fields.Float(required=True, description='The Calendar_definitions Range history periods'),
    'range_future_periods': fields.Float(required=True, description='The Calendar_definitions Range future periods'),
    'freq_period_start_day': fields.String(required=True, description='The Calendar_definitions Freq period start day'),
    'freq_normalize': fields.String(required=True, description='The Calendar_definitions Freq normalize'),
    'freq_closed': fields.String(required=True, description='The Calendar_definitions Freq closed')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

calendar_definitions_agg = api.model('Calendar_definitions_agg', {
    # start new add_agg_argument
    'name_count': fields.Integer(readonly=True, description='The Calendar_definitions Name count'),
    'start_count': fields.Integer(readonly=True, description='The Calendar_definitions Start count'),
    'end_count': fields.Integer(readonly=True, description='The Calendar_definitions End count'),
    'range_history_periods_count': fields.Integer(readonly=True, description='The Calendar_definitions Range history periods count'),
    'range_history_periods_sum': fields.Float(readonly=True, description='The Calendar_definitions Range history periods sum'),
    'range_history_periods_avg': fields.Float(readonly=True, description='The Calendar_definitions Range history periods avg'),
    'range_history_periods_min': fields.Float(readonly=True, description='The Calendar_definitions Range history periods min'),
    'range_history_periods_max': fields.Float(readonly=True, description='The Calendar_definitions Range history periods max'),
    'range_future_periods_count': fields.Integer(readonly=True, description='The Calendar_definitions Range future periods count'),
    'range_future_periods_sum': fields.Float(readonly=True, description='The Calendar_definitions Range future periods sum'),
    'range_future_periods_avg': fields.Float(readonly=True, description='The Calendar_definitions Range future periods avg'),
    'range_future_periods_min': fields.Float(readonly=True, description='The Calendar_definitions Range future periods min'),
    'range_future_periods_max': fields.Float(readonly=True, description='The Calendar_definitions Range future periods max'),
    'freq_period_start_day_count': fields.Integer(readonly=True, description='The Calendar_definitions Freq period start day count'),
    'freq_normalize_count': fields.Integer(readonly=True, description='The Calendar_definitions Freq normalize count'),
    'freq_closed_count': fields.Integer(readonly=True, description='The Calendar_definitions Freq closed count')    # this line should be removed and replaced with the argumentAggParser variable
    # end new add_agg_argument
    # 'name_count': fields.String(required=True, description='The task count')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from Calendar_definitions into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# Calendar_definitions
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single calendar_definitions item, updates a single calendar_definitions item and lets you delete a calendar_definitions item

@ns.route('/<int:id>')
@ns.response(404, 'Calendar_definitions not found')
@ns.param('id', 'The Calendar_definitions identifier')
class Calendar_definitionsResource(Resource):
    '''Show a single Calendar_definitions item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get calendar_definitions')
    @ns.marshal_list_with(calendar_definitions, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self, id):  # /calendar_definitions/<id>
        '''Fetch a single Calendar_definitions item given its identifier'''
        data = Calendar_definitions.query.get_or_404(id)

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete calendar_definitions')
    @ns.doc(security='jwt')
    @jwt_required
    def delete(self, id):  # /calendar_definitions/<id>
        '''Delete a Calendar_definitions given its identifier'''
        data = Calendar_definitions.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Calendar_definitions Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update calendar_definitions')
    @ns.expect(calendar_definitions)
    @ns.marshal_list_with(calendar_definitions, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self, id):  # /calendar_definitions/<id>
        '''Update a Calendar_definitions given its identifier'''
        data = Calendar_definitions.query.get_or_404(id)
        # start update api_request feilds
        data.name = api.payload['name']
        data.start = api.payload['start']
        data.end = api.payload['end']
        data.range_history_periods = api.payload['range_history_periods']
        data.range_future_periods = api.payload['range_future_periods']
        data.freq_period_start_day = api.payload['freq_period_start_day']
        data.freq_normalize = api.payload['freq_normalize']
        data.freq_closed = api.payload['freq_closed']
        # end update api_request feilds
        # data.title = api.payload['title']
        db.session.commit()
        return data, 201


# Calendar_definitionsList
# shows a list of all Calendar_definitions, and lets you POST to add new Calendar_definitions
@ns.route('/')
class Calendar_definitionsListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get calendar_definitions')
    @ns.expect(parser)
    @ns.marshal_list_with(calendar_definitions, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /calendar_definitions
        '''List Calendar_definitions records '''
        args = parser.parse_args()
        page = args['page']

        data = Calendar_definitions.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE']).items

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert calendar_definitions')
    @ns.expect(calendar_definitions)
    @ns.marshal_with(calendar_definitions, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /calendar_definitions
        '''Create a new Calendar_definitions record'''
        data = Calendar_definitions(
            # start new api_request feilds
            name=api.payload['name'],
            start=api.payload['start'],
            end=api.payload['end'],
            range_history_periods=api.payload['range_history_periods'],
            range_future_periods=api.payload['range_future_periods'],
            freq_period_start_day=api.payload['freq_period_start_day'],
            freq_normalize=api.payload['freq_normalize'],
            freq_closed=api.payload['freq_closed']
            # end new api_request feilds
            # title = api.payload['title']
        )
        db.session.add(data)
        db.session.commit()
        return data, 201


# Calendar_definitionsBulk
# Inserts and updates in Bulk of Calendar_definitions, and lets you POST to add and put to update new Calendar_definitions
@ns.route('/bulk')
class Calendar_definitionsBulkListResource(Resource):
    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update calendar_definitions')
    @ns.expect(calendar_definitions)
    @ns.marshal_list_with(calendar_definitions, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self):  # /calendar_definitions/bulk
        '''Bulk update Calendar_definitions given their identifiers'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_update_mappings(Calendar_definitions,data)
        db.session.commit()
        return data, 201

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert calendar_definitions')
    @ns.expect(calendar_definitions)
    @ns.marshal_with(calendar_definitions, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /calendar_definitions/bulk
        '''Bulk create new Calendar_definitions records'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_insert_mappings(Calendar_definitions,data)
        db.session.commit()
        return data, 201


# Calendar_definitionsSeed Data
# Inserts and updates in Bulk of Calendar_definitions, and lets you POST to add and put to update new Calendar_definitions
@ns.route('/seed/<int:level>')
class Calendar_definitionsBulkListResource(Resource):
    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='seed calendar_definitions')
    @ns.expect(calendar_definitions)
    @ns.marshal_with(calendar_definitions, code=201)
    # @ns.doc(security='jwt')
    @ns.doc(security=None)
    # @jwt_required
    def post(self, level):  # /calendar_definitions/seed/<level>
        '''Seed bulk Calendar_definitions records. Level 1 = `Core` Data, Level 2 = `Nice to Have` Data, Level 3 = `Demo` Data'''
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
        db.session.bulk_insert_mappings(Calendar_definitions,data)
        db.session.commit()
        return data, 201


# Calendar_definitionsAggregate
# shows a list of all Calendar_definitions, and lets you POST to add new Calendar_definitions
@ns.route('/aggregate')
class Calendar_definitionsAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get calendar_definitions aggregates')
    @ns.marshal_with(calendar_definitions_agg, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /calendar_definitions
        '''Aggregate Calendar_definitions records '''

        data = Calendar_definitions.query.with_entities(
            
            # start new api_aggregate feilds

                func.count(Calendar_definitions.name).label('name_count'),

                func.count(Calendar_definitions.start).label('start_count'),

                func.count(Calendar_definitions.end).label('end_count'),

                func.count(Calendar_definitions.range_history_periods).label('range_history_periods_count'),

                func.sum(Calendar_definitions.range_history_periods).label('range_history_periods_sum'),

                func.avg(Calendar_definitions.range_history_periods).label('range_history_periods_avg'),

                func.min(Calendar_definitions.range_history_periods).label('range_history_periods_min'),

                func.max(Calendar_definitions.range_history_periods).label('range_history_periods_max'),
                func.count(Calendar_definitions.range_future_periods).label('range_future_periods_count'),

                func.sum(Calendar_definitions.range_future_periods).label('range_future_periods_sum'),

                func.avg(Calendar_definitions.range_future_periods).label('range_future_periods_avg'),

                func.min(Calendar_definitions.range_future_periods).label('range_future_periods_min'),

                func.max(Calendar_definitions.range_future_periods).label('range_future_periods_max'),
                func.count(Calendar_definitions.freq_period_start_day).label('freq_period_start_day_count'),

                func.count(Calendar_definitions.freq_normalize).label('freq_normalize_count'),

                func.count(Calendar_definitions.freq_closed).label('freq_closed_count')
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds

                "name_count":data.name_count,

                "start_count":data.start_count,

                "end_count":data.end_count,

                "range_history_periods_count":data.range_history_periods_count,

                "range_history_periods_sum":data.range_history_periods_sum,

                "range_history_periods_avg":data.range_history_periods_avg,

                "range_history_periods_min":data.range_history_periods_min,

                "range_history_periods_max":data.range_history_periods_max,

                "range_future_periods_count":data.range_future_periods_count,

                "range_future_periods_sum":data.range_future_periods_sum,

                "range_future_periods_avg":data.range_future_periods_avg,

                "range_future_periods_min":data.range_future_periods_min,

                "range_future_periods_max":data.range_future_periods_max,

                "freq_period_start_day_count":data.freq_period_start_day_count,

                "freq_normalize_count":data.freq_normalize_count,

                "freq_closed_count":data.freq_closed_count
            # end new api_aggregate_object feilds
        }

        return data_obj, 200


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Calendar_definitions, "before_insert")
def before_insert(mapper, connection, target):
    if api.payload:
        payload = '{'
        for obj in api.payload:
            payload += '"' + obj + '": "' + api.payload.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_definitions",
            action="Before Insert",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_definitions, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Calendar_definitions, "before_update")
def before_update(mapper, connection, target):
    if api.payload:
        payload = '{'
        for obj in api.payload:
            payload += '"' + obj + '": "' + api.payload.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_definitions",
            action="Before Update",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_definitions, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Calendar_definitions, "before_delete")
def before_delete(mapper, connection, target):
    if api.payload:
        payload = '{'
        for obj in api.payload:
            payload += '"' + obj + '": "' + api.payload.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_definitions",
            action="Before Delete",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_definitions, "after_delete")
def after_delete(mapper, connection, target):
    pass
