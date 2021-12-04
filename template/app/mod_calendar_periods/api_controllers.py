
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
from app.mod_calendar_periods.models import Calendar_periods

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
ns = api.namespace('api/calendar_periods', description='Database model "Calendar_periods", resource based, Api. \
    This API should have 9 endpoints from the name of the model prefixed by "api".\
    There are standard 5 CRUD APIs, a 2 BULK APIs, 1 Seed, and 1 Aggregate')

calendar_periods = api.model('Calendar_periods', {
    'id': fields.Integer(readonly=True, description='The Calendar_periods unique identifier'),
    # start new add_argument
    'calendar_definition_id': fields.Float(required=True, description='The Calendar_periods Calendar definition id'),
    'start_date': fields.String(required=True, description='The Calendar_periods Start date'),
    'end_date': fields.String(required=True, description='The Calendar_periods End date'),
    'day': fields.Float(required=True, description='The Calendar_periods Day'),
    'week': fields.Float(required=True, description='The Calendar_periods Week'),
    'week_day': fields.String(required=True, description='The Calendar_periods Week day'),
    'week_index': fields.Float(required=True, description='The Calendar_periods Week index'),
    'month': fields.Float(required=True, description='The Calendar_periods Month'),
    'month_index': fields.Float(required=True, description='The Calendar_periods Month index'),
    'quarter': fields.Float(required=True, description='The Calendar_periods Quarter'),
    'quarter_index': fields.Float(required=True, description='The Calendar_periods Quarter index'),
    'year': fields.Float(required=True, description='The Calendar_periods Year')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

calendar_periods_agg = api.model('Calendar_periods_agg', {
    # start new add_agg_argument
    'calendar_definition_id_count': fields.Integer(readonly=True, description='The Calendar_periods Calendar definition id count'),
    'calendar_definition_id_sum': fields.Float(readonly=True, description='The Calendar_periods Calendar definition id sum'),
    'calendar_definition_id_avg': fields.Float(readonly=True, description='The Calendar_periods Calendar definition id avg'),
    'calendar_definition_id_min': fields.Float(readonly=True, description='The Calendar_periods Calendar definition id min'),
    'calendar_definition_id_max': fields.Float(readonly=True, description='The Calendar_periods Calendar definition id max'),
    'start_date_count': fields.Integer(readonly=True, description='The Calendar_periods Start date count'),
    'end_date_count': fields.Integer(readonly=True, description='The Calendar_periods End date count'),
    'day_count': fields.Integer(readonly=True, description='The Calendar_periods Day count'),
    'day_sum': fields.Float(readonly=True, description='The Calendar_periods Day sum'),
    'day_avg': fields.Float(readonly=True, description='The Calendar_periods Day avg'),
    'day_min': fields.Float(readonly=True, description='The Calendar_periods Day min'),
    'day_max': fields.Float(readonly=True, description='The Calendar_periods Day max'),
    'week_count': fields.Integer(readonly=True, description='The Calendar_periods Week count'),
    'week_sum': fields.Float(readonly=True, description='The Calendar_periods Week sum'),
    'week_avg': fields.Float(readonly=True, description='The Calendar_periods Week avg'),
    'week_min': fields.Float(readonly=True, description='The Calendar_periods Week min'),
    'week_max': fields.Float(readonly=True, description='The Calendar_periods Week max'),
    'week_day_count': fields.Integer(readonly=True, description='The Calendar_periods Week day count'),
    'week_index_count': fields.Integer(readonly=True, description='The Calendar_periods Week index count'),
    'week_index_sum': fields.Float(readonly=True, description='The Calendar_periods Week index sum'),
    'week_index_avg': fields.Float(readonly=True, description='The Calendar_periods Week index avg'),
    'week_index_min': fields.Float(readonly=True, description='The Calendar_periods Week index min'),
    'week_index_max': fields.Float(readonly=True, description='The Calendar_periods Week index max'),
    'month_count': fields.Integer(readonly=True, description='The Calendar_periods Month count'),
    'month_sum': fields.Float(readonly=True, description='The Calendar_periods Month sum'),
    'month_avg': fields.Float(readonly=True, description='The Calendar_periods Month avg'),
    'month_min': fields.Float(readonly=True, description='The Calendar_periods Month min'),
    'month_max': fields.Float(readonly=True, description='The Calendar_periods Month max'),
    'month_index_count': fields.Integer(readonly=True, description='The Calendar_periods Month index count'),
    'month_index_sum': fields.Float(readonly=True, description='The Calendar_periods Month index sum'),
    'month_index_avg': fields.Float(readonly=True, description='The Calendar_periods Month index avg'),
    'month_index_min': fields.Float(readonly=True, description='The Calendar_periods Month index min'),
    'month_index_max': fields.Float(readonly=True, description='The Calendar_periods Month index max'),
    'quarter_count': fields.Integer(readonly=True, description='The Calendar_periods Quarter count'),
    'quarter_sum': fields.Float(readonly=True, description='The Calendar_periods Quarter sum'),
    'quarter_avg': fields.Float(readonly=True, description='The Calendar_periods Quarter avg'),
    'quarter_min': fields.Float(readonly=True, description='The Calendar_periods Quarter min'),
    'quarter_max': fields.Float(readonly=True, description='The Calendar_periods Quarter max'),
    'quarter_index_count': fields.Integer(readonly=True, description='The Calendar_periods Quarter index count'),
    'quarter_index_sum': fields.Float(readonly=True, description='The Calendar_periods Quarter index sum'),
    'quarter_index_avg': fields.Float(readonly=True, description='The Calendar_periods Quarter index avg'),
    'quarter_index_min': fields.Float(readonly=True, description='The Calendar_periods Quarter index min'),
    'quarter_index_max': fields.Float(readonly=True, description='The Calendar_periods Quarter index max'),
    'year_count': fields.Integer(readonly=True, description='The Calendar_periods Year count'),
    'year_sum': fields.Float(readonly=True, description='The Calendar_periods Year sum'),
    'year_avg': fields.Float(readonly=True, description='The Calendar_periods Year avg'),
    'year_min': fields.Float(readonly=True, description='The Calendar_periods Year min'),
    'year_max': fields.Float(readonly=True, description='The Calendar_periods Year max')    # this line should be removed and replaced with the argumentAggParser variable
    # end new add_agg_argument
    # 'name_count': fields.String(required=True, description='The task count')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from Calendar_periods into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# Calendar_periods
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single calendar_periods item, updates a single calendar_periods item and lets you delete a calendar_periods item

@ns.route('/<int:id>')
@ns.response(404, 'Calendar_periods not found')
@ns.param('id', 'The Calendar_periods identifier')
class Calendar_periodsResource(Resource):
    '''Show a single Calendar_periods item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get calendar_periods')
    @ns.marshal_list_with(calendar_periods, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self, id):  # /calendar_periods/<id>
        '''Fetch a single Calendar_periods item given its identifier'''
        data = Calendar_periods.query.get_or_404(id)

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete calendar_periods')
    @ns.doc(security='jwt')
    @jwt_required
    def delete(self, id):  # /calendar_periods/<id>
        '''Delete a Calendar_periods given its identifier'''
        data = Calendar_periods.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Calendar_periods Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update calendar_periods')
    @ns.expect(calendar_periods)
    @ns.marshal_list_with(calendar_periods, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self, id):  # /calendar_periods/<id>
        '''Update a Calendar_periods given its identifier'''
        data = Calendar_periods.query.get_or_404(id)
        # start update api_request feilds
        data.calendar_definition_id = api.payload['calendar_definition_id']
        data.start_date = api.payload['start_date']
        data.end_date = api.payload['end_date']
        data.day = api.payload['day']
        data.week = api.payload['week']
        data.week_day = api.payload['week_day']
        data.week_index = api.payload['week_index']
        data.month = api.payload['month']
        data.month_index = api.payload['month_index']
        data.quarter = api.payload['quarter']
        data.quarter_index = api.payload['quarter_index']
        data.year = api.payload['year']
        # end update api_request feilds
        # data.title = api.payload['title']
        db.session.commit()
        return data, 201


# Calendar_periodsList
# shows a list of all Calendar_periods, and lets you POST to add new Calendar_periods
@ns.route('/')
class Calendar_periodsListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get calendar_periods')
    @ns.expect(parser)
    @ns.marshal_list_with(calendar_periods, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /calendar_periods
        '''List Calendar_periods records '''
        args = parser.parse_args()
        page = args['page']

        data = Calendar_periods.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE']).items

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert calendar_periods')
    @ns.expect(calendar_periods)
    @ns.marshal_with(calendar_periods, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /calendar_periods
        '''Create a new Calendar_periods record'''
        data = Calendar_periods(
            # start new api_request feilds
            calendar_definition_id=api.payload['calendar_definition_id'],
            start_date=api.payload['start_date'],
            end_date=api.payload['end_date'],
            day=api.payload['day'],
            week=api.payload['week'],
            week_day=api.payload['week_day'],
            week_index=api.payload['week_index'],
            month=api.payload['month'],
            month_index=api.payload['month_index'],
            quarter=api.payload['quarter'],
            quarter_index=api.payload['quarter_index'],
            year=api.payload['year']
            # end new api_request feilds
            # title = api.payload['title']
        )
        db.session.add(data)
        db.session.commit()
        return data, 201


# Calendar_periodsBulk
# Inserts and updates in Bulk of Calendar_periods, and lets you POST to add and put to update new Calendar_periods
@ns.route('/bulk')
class Calendar_periodsBulkListResource(Resource):
    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update calendar_periods')
    @ns.expect(calendar_periods)
    @ns.marshal_list_with(calendar_periods, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self):  # /calendar_periods/bulk
        '''Bulk update Calendar_periods given their identifiers'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_update_mappings(Calendar_periods,data)
        db.session.commit()
        return data, 201

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert calendar_periods')
    @ns.expect(calendar_periods)
    @ns.marshal_with(calendar_periods, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /calendar_periods/bulk
        '''Bulk create new Calendar_periods records'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_insert_mappings(Calendar_periods,data)
        db.session.commit()
        return data, 201


# Calendar_periodsSeed Data
# Inserts and updates in Bulk of Calendar_periods, and lets you POST to add and put to update new Calendar_periods
@ns.route('/seed/<int:level>')
class Calendar_periodsBulkSeedResource(Resource):
    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='seed calendar_periods')
    # @ns.expect(calendar_periods)
    # @ns.marshal_with(calendar_periods, code=201)
    # @ns.doc(security='jwt')
    @ns.doc(security=None)
    # @jwt_required
    def get(self, level):  # /calendar_periods/seed/<level>
        '''Seed bulk Calendar_periods records. Level 1 = `Core` Data, Level 2 = `Nice to Have` Data, Level 3 = `Demo` Data'''
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
        db.session.bulk_insert_mappings(Calendar_periods,data)
        db.session.commit()
        return data, 201


# Calendar_periodsAggregate
# shows a list of all Calendar_periods, and lets you POST to add new Calendar_periods
@ns.route('/aggregate')
class Calendar_periodsAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get calendar_periods aggregates')
    @ns.marshal_with(calendar_periods_agg, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /calendar_periods
        '''Aggregate Calendar_periods records '''

        data = Calendar_periods.query.with_entities(
            
            # start new api_aggregate feilds

                func.count(Calendar_periods.calendar_definition_id).label('calendar_definition_id_count'),

                func.sum(Calendar_periods.calendar_definition_id).label('calendar_definition_id_sum'),

                func.avg(Calendar_periods.calendar_definition_id).label('calendar_definition_id_avg'),

                func.min(Calendar_periods.calendar_definition_id).label('calendar_definition_id_min'),

                func.max(Calendar_periods.calendar_definition_id).label('calendar_definition_id_max'),
                func.count(Calendar_periods.start_date).label('start_date_count'),

                func.count(Calendar_periods.end_date).label('end_date_count'),

                func.count(Calendar_periods.day).label('day_count'),

                func.sum(Calendar_periods.day).label('day_sum'),

                func.avg(Calendar_periods.day).label('day_avg'),

                func.min(Calendar_periods.day).label('day_min'),

                func.max(Calendar_periods.day).label('day_max'),
                func.count(Calendar_periods.week).label('week_count'),

                func.sum(Calendar_periods.week).label('week_sum'),

                func.avg(Calendar_periods.week).label('week_avg'),

                func.min(Calendar_periods.week).label('week_min'),

                func.max(Calendar_periods.week).label('week_max'),
                func.count(Calendar_periods.week_day).label('week_day_count'),

                func.count(Calendar_periods.week_index).label('week_index_count'),

                func.sum(Calendar_periods.week_index).label('week_index_sum'),

                func.avg(Calendar_periods.week_index).label('week_index_avg'),

                func.min(Calendar_periods.week_index).label('week_index_min'),

                func.max(Calendar_periods.week_index).label('week_index_max'),
                func.count(Calendar_periods.month).label('month_count'),

                func.sum(Calendar_periods.month).label('month_sum'),

                func.avg(Calendar_periods.month).label('month_avg'),

                func.min(Calendar_periods.month).label('month_min'),

                func.max(Calendar_periods.month).label('month_max'),
                func.count(Calendar_periods.month_index).label('month_index_count'),

                func.sum(Calendar_periods.month_index).label('month_index_sum'),

                func.avg(Calendar_periods.month_index).label('month_index_avg'),

                func.min(Calendar_periods.month_index).label('month_index_min'),

                func.max(Calendar_periods.month_index).label('month_index_max'),
                func.count(Calendar_periods.quarter).label('quarter_count'),

                func.sum(Calendar_periods.quarter).label('quarter_sum'),

                func.avg(Calendar_periods.quarter).label('quarter_avg'),

                func.min(Calendar_periods.quarter).label('quarter_min'),

                func.max(Calendar_periods.quarter).label('quarter_max'),
                func.count(Calendar_periods.quarter_index).label('quarter_index_count'),

                func.sum(Calendar_periods.quarter_index).label('quarter_index_sum'),

                func.avg(Calendar_periods.quarter_index).label('quarter_index_avg'),

                func.min(Calendar_periods.quarter_index).label('quarter_index_min'),

                func.max(Calendar_periods.quarter_index).label('quarter_index_max'),
                func.count(Calendar_periods.year).label('year_count'),

                func.sum(Calendar_periods.year).label('year_sum'),

                func.avg(Calendar_periods.year).label('year_avg'),

                func.min(Calendar_periods.year).label('year_min'),

                func.max(Calendar_periods.year).label('year_max')
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds

                "calendar_definition_id_count":data.calendar_definition_id_count,

                "calendar_definition_id_sum":data.calendar_definition_id_sum,

                "calendar_definition_id_avg":data.calendar_definition_id_avg,

                "calendar_definition_id_min":data.calendar_definition_id_min,

                "calendar_definition_id_max":data.calendar_definition_id_max,

                "start_date_count":data.start_date_count,

                "end_date_count":data.end_date_count,

                "day_count":data.day_count,

                "day_sum":data.day_sum,

                "day_avg":data.day_avg,

                "day_min":data.day_min,

                "day_max":data.day_max,

                "week_count":data.week_count,

                "week_sum":data.week_sum,

                "week_avg":data.week_avg,

                "week_min":data.week_min,

                "week_max":data.week_max,

                "week_day_count":data.week_day_count,

                "week_index_count":data.week_index_count,

                "week_index_sum":data.week_index_sum,

                "week_index_avg":data.week_index_avg,

                "week_index_min":data.week_index_min,

                "week_index_max":data.week_index_max,

                "month_count":data.month_count,

                "month_sum":data.month_sum,

                "month_avg":data.month_avg,

                "month_min":data.month_min,

                "month_max":data.month_max,

                "month_index_count":data.month_index_count,

                "month_index_sum":data.month_index_sum,

                "month_index_avg":data.month_index_avg,

                "month_index_min":data.month_index_min,

                "month_index_max":data.month_index_max,

                "quarter_count":data.quarter_count,

                "quarter_sum":data.quarter_sum,

                "quarter_avg":data.quarter_avg,

                "quarter_min":data.quarter_min,

                "quarter_max":data.quarter_max,

                "quarter_index_count":data.quarter_index_count,

                "quarter_index_sum":data.quarter_index_sum,

                "quarter_index_avg":data.quarter_index_avg,

                "quarter_index_min":data.quarter_index_min,

                "quarter_index_max":data.quarter_index_max,

                "year_count":data.year_count,

                "year_sum":data.year_sum,

                "year_avg":data.year_avg,

                "year_min":data.year_min,

                "year_max":data.year_max
            # end new api_aggregate_object feilds
        }

        return data_obj, 200


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Calendar_periods, "before_insert")
def before_insert(mapper, connection, target):
    if api.payload:
        payload = '{'
        for obj in api.payload:
            payload += '"' + obj + '": "' + api.payload.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_periods",
            action="Before Insert",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_periods, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Calendar_periods, "before_update")
def before_update(mapper, connection, target):
    if api.payload:
        payload = '{'
        for obj in api.payload:
            payload += '"' + obj + '": "' + api.payload.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_periods",
            action="Before Update",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_periods, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Calendar_periods, "before_delete")
def before_delete(mapper, connection, target):
    if api.payload:
        payload = '{'
        for obj in api.payload:
            payload += '"' + obj + '": "' + api.payload.get(obj) + '",'
        payload = payload.rstrip(',')
        payload += '}'
        
        data = Audit(
            model_name="Calendar_periods",
            action="Before Delete",
            context="Rest API",
            payload=payload
        )
        db.session.add(data)
    pass


@event.listens_for(Calendar_periods, "after_delete")
def after_delete(mapper, connection, target):
    pass
