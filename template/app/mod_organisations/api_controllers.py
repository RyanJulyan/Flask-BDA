
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

# Import module models (i.e. User)
from app.mod_organisations.models import Organisations

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
ns = api.namespace('api/organisations', description='Database model "Organisations", resource based, Api. \
    This API should have 2 endpoints from the name of the model prefixed by "api".')

organisations = api.model('Organisations', {
    'id': fields.Integer(readonly=True, description='The Organisations unique identifier'),
    # start new add_argument
    'organisation_name': fields.String(required=True, description='The Organisations Organisation name'),
    'organisation_logo': fields.String(description='The Organisations Organisation logo'),
    'organisation_description': fields.String(description='The Organisations Organisation description'),
    'organisation_industry': fields.String(description='The Organisations Organisation industry'),
    'organisation_contact_name': fields.String(required=True, description='The Organisations Organisation contact name'),
    'organisation_contact_email': fields.String(required=True, description='The Organisations Organisation contact email'),
    'organisation_binding_database_uri': fields.String(required=True, description='The Organisations Organisation binding database uri'),
    'organisation_address': fields.String(description='The Organisations Organisation address'),
    'organisation_city': fields.String(description='The Organisations Organisation city'),
    'organisation_postal_code': fields.String(description='The Organisations Organisation postal code'),
    'organisation_country': fields.String(description='The Organisations Organisation country'),
    'organisation_homepage': fields.String(description='The Organisations Organisation homepage'),
    'organisation_vat_number': fields.String(description='The Organisations Organisation vat number'),
    'organisation_reg_number': fields.String(description='The Organisations Organisation reg number')
    # end new add_argument
    # 'task': fields.String(required=True, description='The task details')
})

organisations_agg = api.model('Organisations_agg', {
    # start new add_agg_argument
    'organisation_name_count': fields.Integer(readonly=True, description='The Organisations Organisation name count'),
    'organisation_logo_count': fields.Integer(readonly=True, description='The Organisations Organisation logo count'),
    'organisation_description_count': fields.Integer(readonly=True, description='The Organisations Organisation description count'),
    'organisation_industry_count': fields.Integer(readonly=True, description='The Organisations Organisation industry count'),
    'organisation_contact_name_count': fields.Integer(readonly=True, description='The Organisations Organisation contact name count'),
    'organisation_contact_email_count': fields.Integer(readonly=True, description='The Organisations Organisation contact email count'),
    'organisation_binding_database_uri_count': fields.Integer(readonly=True, description='The Organisations Organisation binding database uri count'),
    'organisation_address_count': fields.Integer(readonly=True, description='The Organisations Organisation address count'),
    'organisation_city_count': fields.Integer(readonly=True, description='The Organisations Organisation city count'),
    'organisation_postal_code_count': fields.Integer(readonly=True, description='The Organisations Organisation postal code count'),
    'organisation_country_count': fields.Integer(readonly=True, description='The Organisations Organisation country count'),
    'organisation_homepage_count': fields.Integer(readonly=True, description='The Organisations Organisation homepage count'),
    'organisation_vat_number_count': fields.Integer(readonly=True, description='The Organisations Organisation vat number count'),
    'organisation_reg_number_count': fields.Integer(readonly=True, description='The Organisations Organisation reg number count')    # this line should be removed and replaced with the argumentAggParser variable
    # end new add_agg_argument
    # 'name_count': fields.String(required=True, description='The task count')
})

# Addtional query string arguements from URL
parser = reqparse.RequestParser()
parser.add_argument('page', type=int, help='page number for returned list. Must be an Integer. Used for dividing returned values from Organisations into pages. Returning up to ' + str(app.config['ROWS_PER_PAGE']) + 'records')
# parser.add_argument('example')

# Organisations
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://github.com/python-restx/flask-restx#quick-start for API and Swagger
# shows a single organisations item, updates a single organisations item and lets you delete a organisations item

@ns.route('/<int:id>')
@ns.response(404, 'Organisations not found')
@ns.param('id', 'The Organisations identifier')
class OrganisationsResource(Resource):
    '''Show a single Organisations item and lets you delete them'''
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get organisations')
    @ns.marshal_list_with(organisations, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self, id):  # /organisations/<id>
        '''Fetch a single Organisations item given its identifier'''
        data = Organisations.query.get_or_404(id)

        return data, 200

    @ns.doc(responses={204: 'DELETED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='delete organisations')
    @ns.doc(security='jwt')
    @jwt_required
    def delete(self, id):  # /organisations/<id>
        '''Delete a Organisations given its identifier'''
        data = Organisations.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()
        return 'Deleted Organisations Record', 204

    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update organisations')
    @ns.expect(organisations)
    @ns.marshal_list_with(organisations, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self, id):  # /organisations/<id>
        '''Update a Organisations given its identifier'''
        data = Organisations.query.get_or_404(id)
        # start update api_request feilds
        data.organisation_name = api.payload['organisation_name']
        data.organisation_logo = api.payload['organisation_logo']
        data.organisation_description = api.payload['organisation_description']
        data.organisation_industry = api.payload['organisation_industry']
        data.organisation_contact_name = api.payload['organisation_contact_name']
        data.organisation_contact_email = api.payload['organisation_contact_email']
        data.organisation_binding_database_uri = api.payload['organisation_binding_database_uri']
        data.organisation_address = api.payload['organisation_address']
        data.organisation_city = api.payload['organisation_city']
        data.organisation_postal_code = api.payload['organisation_postal_code']
        data.organisation_country = api.payload['organisation_country']
        data.organisation_homepage = api.payload['organisation_homepage']
        data.organisation_vat_number = api.payload['organisation_vat_number']
        data.organisation_reg_number = api.payload['organisation_reg_number']
        # end update api_request feilds
        # data.title = api.payload['title']
        db.session.commit()
        return data, 201


# OrganisationsList
# shows a list of all Organisations, and lets you POST to add new Organisations
@ns.route('/')
class OrganisationsListResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get organisations')
    @ns.expect(parser)
    @ns.marshal_list_with(organisations, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /organisations
        '''List Organisations records '''
        args = parser.parse_args()
        page = args['page']

        data = Organisations.query.paginate(page=page, per_page=app.config['ROWS_PER_PAGE']).items

        return data, 200

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert organisations')
    @ns.expect(organisations)
    @ns.marshal_with(organisations, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /organisations
        '''Create a new Organisations record'''
        data = Organisations(
            # start new api_request feilds
            organisation_name=api.payload['organisation_name'],
            organisation_logo=api.payload['organisation_logo'],
            organisation_description=api.payload['organisation_description'],
            organisation_industry=api.payload['organisation_industry'],
            organisation_contact_name=api.payload['organisation_contact_name'],
            organisation_contact_email=api.payload['organisation_contact_email'],
            organisation_binding_database_uri=api.payload['organisation_binding_database_uri'],
            organisation_address=api.payload['organisation_address'],
            organisation_city=api.payload['organisation_city'],
            organisation_postal_code=api.payload['organisation_postal_code'],
            organisation_country=api.payload['organisation_country'],
            organisation_homepage=api.payload['organisation_homepage'],
            organisation_vat_number=api.payload['organisation_vat_number'],
            organisation_reg_number=api.payload['organisation_reg_number']
            # end new api_request feilds
            # title = api.payload['title']
        )
        db.session.add(data)
        db.session.commit()
        return data, 201


# OrganisationsBulk
# Inserts and updates in Bulk of Organisations, and lets you POST to add and put to update new Organisations
@ns.route('/bulk')
class OrganisationsBulkListResource(Resource):
    @ns.doc(responses={201: 'UPDATED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='update organisations')
    @ns.expect(organisations)
    @ns.marshal_list_with(organisations, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def put(self):  # /organisations/bulk
        '''Bulk update Organisations given their identifiers'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_update_mappings(Organisations,data)
        db.session.commit()
        return data, 201

    @ns.doc(responses={201: 'INSERTED', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='insert organisations')
    @ns.expect(organisations)
    @ns.marshal_with(organisations, code=201)
    @ns.doc(security='jwt')
    @jwt_required
    def post(self):  # /organisations/bulk
        '''Bulk create new Organisations records'''
        data = json.dumps(api.payload)
        # data = read_json(data, convert_dates=['start_date'])
        data = read_json(data)
        data = data.to_dict(orient="records")
        db.session.bulk_insert_mappings(Organisations,data)
        db.session.commit()
        return data, 201


# OrganisationsAggregate
# shows a list of all Organisations, and lets you POST to add new Organisations
@ns.route('/aggregate')
class OrganisationsAggregateResource(Resource):
    @ns.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
             description='get organisations aggregates')
    @ns.marshal_with(organisations_agg, code=200)
    @ns.doc(security='jwt')
    @jwt_required
    def get(self):  # /organisations
        '''Aggregate Organisations records '''

        data = Organisations.query.with_entities(
            
            # start new api_aggregate feilds

                func.count(Organisations.organisation_name).label('organisation_name_count'),

                func.count(Organisations.organisation_logo).label('organisation_logo_count'),

                func.count(Organisations.organisation_description).label('organisation_description_count'),

                func.count(Organisations.organisation_industry).label('organisation_industry_count'),

                func.count(Organisations.organisation_contact_name).label('organisation_contact_name_count'),

                func.count(Organisations.organisation_contact_email).label('organisation_contact_email_count'),

                func.count(Organisations.organisation_binding_database_uri).label('organisation_binding_database_uri_count'),

                func.count(Organisations.organisation_address).label('organisation_address_count'),

                func.count(Organisations.organisation_city).label('organisation_city_count'),

                func.count(Organisations.organisation_postal_code).label('organisation_postal_code_count'),

                func.count(Organisations.organisation_country).label('organisation_country_count'),

                func.count(Organisations.organisation_homepage).label('organisation_homepage_count'),

                func.count(Organisations.organisation_vat_number).label('organisation_vat_number_count'),

                func.count(Organisations.organisation_reg_number).label('organisation_reg_number_count')
            # end new api_aggregate feilds
            
        ).first()

        data_obj = {
            
            # start new api_aggregate_object feilds

                "organisation_name_count":data.organisation_name_count,

                "organisation_logo_count":data.organisation_logo_count,

                "organisation_description_count":data.organisation_description_count,

                "organisation_industry_count":data.organisation_industry_count,

                "organisation_contact_name_count":data.organisation_contact_name_count,

                "organisation_contact_email_count":data.organisation_contact_email_count,

                "organisation_binding_database_uri_count":data.organisation_binding_database_uri_count,

                "organisation_address_count":data.organisation_address_count,

                "organisation_city_count":data.organisation_city_count,

                "organisation_postal_code_count":data.organisation_postal_code_count,

                "organisation_country_count":data.organisation_country_count,

                "organisation_homepage_count":data.organisation_homepage_count,

                "organisation_vat_number_count":data.organisation_vat_number_count,

                "organisation_reg_number_count":data.organisation_reg_number_count
            # end new api_aggregate_object feilds
        }

        return data_obj, 200


# SQLAlchemy Events before and after insert, update and delete changes on a table
@event.listens_for(Organisations, "before_insert")
def before_insert(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Organisations",
        action="Before Insert",
        context="Rest API",
        payload=payload
    )
    db.session.add(data)
    db.session.commit()
    pass


@event.listens_for(Organisations, "after_insert")
def after_insert(mapper, connection, target):
    pass


@event.listens_for(Organisations, "before_update")
def before_update(mapper, connection, target):
    payload = '{'
    for obj in request.form:
        payload += '"' + obj + '": "' + request.form.get(obj) + '",'
    payload = payload.rstrip(',')
    payload += '}'
    
    data = Audit(
        model_name="Organisations",
        action="Before Update",
        context="Rest API",
        payload=payload
    )
    db.session.add(data)
    db.session.commit()
    pass


@event.listens_for(Organisations, "after_update")
def after_update(mapper, connection, target):
    pass


@event.listens_for(Organisations, "before_delete")
def before_delete(mapper, connection, target):
    pass


@event.listens_for(Organisations, "after_delete")
def after_delete(mapper, connection, target):
    pass
