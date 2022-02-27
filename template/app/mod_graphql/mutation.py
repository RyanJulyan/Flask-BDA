import graphene

from app import db

# Import GraphQLAuth
# from flask_graphql_auth import create_access_token, create_refresh_token, mutation_jwt_required
# Import GraphQL global node id
from graphql_relay.node.node import from_global_id

# Import Models and Types
# users
from app.mod_users.models import Users as UsersModel
from app.mod_users.types import Users as UsersTypes, CreateUserInput
# web_hooks
from app.mod_web_hooks.models import Web_hooks as Web_hooksModel  # noqa: E402
from app.mod_web_hooks.types import Web_hooks as Web_hooksTypes, CreateWeb_hooksInput  # noqa: E402
# calendar_definitions
from app.mod_calendar_definitions.models import Calendar_definitions as Calendar_definitionsModel  # noqa: E402
from app.mod_calendar_definitions.types import Calendar_definitions as Calendar_definitionsTypes, CreateCalendar_definitionsInput  # noqa: E402
# calendar_periods
from app.mod_calendar_periods.models import Calendar_periods as Calendar_periodsModel  # noqa: E402
from app.mod_calendar_periods.types import Calendar_periods as Calendar_periodsTypes, CreateCalendar_periodsInput  # noqa: E402
# import new xyz_model and xyz_type, input
# statuses
from app.mod_statuses.models import Statuses as StatusesModel  # noqa: E402
from app.mod_statuses.types import Statuses as StatusesTypes, CreateStatusesInput  # noqa: E402


def graphql_input_into_dictionary(input):
    """Method to convert Graphene inputs into dictionary"""
    dictionary = {}
    for key in input:
        # Convert GraphQL global id to database id
        if key[-2:] == 'id':
            input[key] = from_global_id(input[key])[1]
        dictionary[key] = input[key]
    return dictionary


class Create_User(graphene.Mutation):
    user = graphene.Field(lambda: UsersTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateUserInput(required=True)

    @staticmethod
    # @mutation_jwt_required
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        user = UsersModel(**data)
        db.session.add(user)
        db.session.commit()
        ok = True
        return Create_User(user=user, ok=ok)


class AuthMutation(graphene.Mutation):
    access_token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        email = graphene.String()
        password = graphene.String()
    
    def mutate(self, info , username, password) :
        user = UsersModel.query.filter_by(email=email,password=password).first()
        if not user:
            raise Exception('Authenication Failure : User is not registered')
        return AuthMutation(
            access_token = create_access_token(email),
            refresh_token = create_refresh_token(email)
        )


# statuses
class Create_Statuses(graphene.Mutation):
    statuses = graphene.Field(lambda: StatusesTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateStatusesInput(required=True)

    
    @staticmethod
    # @mutation_jwt_required
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        statuses = StatusesModel(**data)
        db.session.add(statuses)
        db.session.commit()
        ok = True
        return Create_Statuses(statuses=statuses, ok=ok)


# web_hooks
class Create_Web_hooks(graphene.Mutation):
    web_hooks = graphene.Field(lambda: Web_hooksTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateWeb_hooksInput(required=True)

    @staticmethod
    # @mutation_jwt_required
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        web_hooks = Web_hooksModel(**data)
        db.session.add(web_hooks)
        db.session.commit()
        ok = True
        return Create_Web_hooks(web_hooks=web_hooks, ok=ok)

            
# calendar_definitions
class Create_Calendar_definitions(graphene.Mutation):
    calendar_definitions = graphene.Field(lambda: Calendar_definitionsTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateCalendar_definitionsInput(required=True)

    @staticmethod
    # @mutation_jwt_required
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        calendar_definitions = Calendar_definitionsModel(**data)
        db.session.add(calendar_definitions)
        db.session.commit()
        ok = True
        return Create_Calendar_definitions(calendar_definitions=calendar_definitions, ok=ok)


# calendar_periods
class Create_Calendar_periods(graphene.Mutation):
    calendar_periods = graphene.Field(lambda: Calendar_periodsTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateCalendar_periodsInput(required=True)

    @staticmethod
    # @mutation_jwt_required
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        calendar_periods = Calendar_periodsModel(**data)
        db.session.add(calendar_periods)
        db.session.commit()
        ok = True
        return Create_Calendar_periods(calendar_periods=calendar_periods, ok=ok)


# new create xyz class
            
            
class Mutation(graphene.ObjectType):
    createUser = Create_User.Field()
    auth = AuthMutation.Field()
    # statuses
    createStatuses = Create_Statuses.Field()
    # web_hooks
    createWeb_hooks = Create_Web_hooks.Field()
    # calendar_definitions
    createCalendar_definitions = Create_Calendar_definitions.Field()
    # calendar_periods
    createCalendar_periods = Create_Calendar_periods.Field()
    # register new createXyz

