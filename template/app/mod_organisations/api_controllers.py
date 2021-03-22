
# Import Flask Resource, fields from flask_restx for API and Swagger
from flask_restx import Resource, fields, reqparse
# Import sql functions (SUM,MIN,MAX,AVG)
from sqlalchemy.sql import func

# JWT for API
from flask_jwt_extended import jwt_required

# Import the database object from the main app module
from app import db, app, api

# Import module models (i.e. User)
from app.mod_organisations.models import Organisations

# Swagger namespace
ns = api.namespace('api/organisations', description='Database model "Organisations", resource based, Api. \
    This API should have 2 endpoints from the name of the model prefixed by "api".')

organisations = api.model('Organisations', {
    'id': fields.Integer(readonly=True, description='The Organisations unique identifier'),
    # start new add_argument
    'organisation_name': fields.String(required=True, description='The Organisations Organisation name'),
    'organisation_details': fields.String(description='The Organisations Organisation details'),
    'organisation_contact_name': fields.String(required=True, description='The Organisations Organisation contact name'),
    'organisation_contact_email': fields.String(required=True, description='The Organisations Organisation contact email'),
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
    'organisation_details_count': fields.Integer(readonly=True, description='The Organisations Organisation details count'),
    'organisation_contact_name_count': fields.Integer(readonly=True, description='The Organisations Organisation contact name count'),
    'organisation_contact_email_count': fields.Integer(readonly=True, description='The Organisations Organisation contact email count'),
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
        data.organisation_details = api.payload['organisation_details']
        data.organisation_contact_name = api.payload['organisation_contact_name']
        data.organisation_contact_email = api.payload['organisation_contact_email']
        data.organisation_address = api.payload['organisation_address']
        data.organisation_city = api.payload['organisation_city']
        data.organisation_postal_code = api.payload['organisation_postal_code']
        data.organisation_country = api.payload['organisation_country']
        data.organisation_homepage = api.payload['organisation_homepage']
        data.organisation_vat_number = api.payload['organisation_vat_number']
        data.organisation_reg_number = api.payload['organisation_reg_number']
        # end update api_request feilds
        db.session.commit()
        db.session.refresh(data)
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
        args = parser.parse_args()
        data = Organisations(
            # start new api_request feilds
            organisation_name=api.payload['organisation_name'],
            organisation_details=api.payload['organisation_details'],
            organisation_contact_name=api.payload['organisation_contact_name'],
            organisation_contact_email=api.payload['organisation_contact_email'],
            organisation_address=api.payload['organisation_address'],
            organisation_city=api.payload['organisation_city'],
            organisation_postal_code=api.payload['organisation_postal_code'],
            organisation_country=api.payload['organisation_country'],
            organisation_homepage=api.payload['organisation_homepage'],
            organisation_vat_number=api.payload['organisation_vat_number'],
            organisation_reg_number=api.payload['organisation_reg_number']
            # end new api_request feilds
            # title=args['title']
        )
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
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

            func.count(Organisations.organisation_contact_name).label('organisation_contact_name_count'),

            func.count(Organisations.organisation_details).label('organisation_details_count'),

            func.count(Organisations.organisation_contact_email).label('organisation_contact_email_count'),

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

            "organisation_contact_name_count":data.organisation_contact_name_count,

            "organisation_details_count":data.organisation_details_count,

            "organisation_contact_email_count":data.organisation_contact_email_count,

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