
import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
# from flask_graphql_auth import query_header_jwt_required

# Import Models and Types
# users
from app.mod_users.models import Users as UsersModel
from app.mod_users.types import Users as UsersTypes
# web_hooks
from app.mod_web_hooks.models import Web_hooks as Web_hooksModel  # noqa: E402
from app.mod_web_hooks.types import Web_hooks as Web_hooksTypes  # noqa: E402
# calendar_definitions
from app.mod_calendar_definitions.models import Calendar_definitions as Calendar_definitionsModel  # noqa: E402
from app.mod_calendar_definitions.types import Calendar_definitions as Calendar_definitionsTypes  # noqa: E402
# calendar_periods
from app.mod_calendar_periods.models import Calendar_periods as Calendar_periodsModel  # noqa: E402
from app.mod_calendar_periods.types import Calendar_periods as Calendar_periodsTypes  # noqa: E402
# import new xyz_model and xyz_type
# api_keys
from app.mod_api_keys.models import Api_keys as Api_keysModel  # noqa: E402
from app.mod_api_keys.types import Api_keys as Api_keysTypes  # noqa: E402
# api_keys
from app.mod_api_keys.models import Api_keys as Api_keysModel  # noqa: E402
from app.mod_api_keys.types import Api_keys as Api_keysTypes  # noqa: E402
# test
from app.mod_test.models import Test as TestModel  # noqa: E402
from app.mod_test.types import Test as TestTypes  # noqa: E402
# statuses
from app.mod_statuses.models import Statuses as StatusesModel  # noqa: E402
from app.mod_statuses.types import Statuses as StatusesTypes  # noqa: E402


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    # @query_header_jwt_required
    all_users = SQLAlchemyConnectionField(UsersTypes.connection)
    # statuses
    # @query_header_jwt_required
    all_statuses = SQLAlchemyConnectionField(StatusesTypes.connection)
    # web_hooks
    # @query_header_jwt_required
    all_web_hooks = SQLAlchemyConnectionField(Web_hooksTypes.connection)
    # calendar_definitions
    # @query_header_jwt_required
    all_calendar_definitions = SQLAlchemyConnectionField(Calendar_definitionsTypes.connection)
    # calendar_periods
    # @query_header_jwt_required
    all_calendar_periods = SQLAlchemyConnectionField(Calendar_periodsTypes.connection)
    # new xyz_model connection
    # api_keys
    all_api_keys = SQLAlchemyConnectionField(Api_keysTypes.connection)
    # api_keys
    all_api_keys = SQLAlchemyConnectionField(Api_keysTypes.connection)
    # test
    all_test = SQLAlchemyConnectionField(TestTypes.connection)

    users_by_name = graphene.List(UsersTypes, name=graphene.String())

    @staticmethod
    def resolve_users_by_name(parent, info, **args):
        q = args.get('name')

        query = UsersModel.get_query(info)

        return query.filter(UsersModel.name.contains(q)).all()

    get_user = graphene.Field(type=UsersTypes, token=graphene.String(),id=graphene.Int())
    
    # @query_header_jwt_required
    def resolve_get_user(self,info,id):
        user_qry = UsersTypes.get_query(info)
        user_val = user_qry.filter(UsersModel.id.contains(id)).first()
        return user_val