import graphene

from app import db

# Import GraphQLAuth
from flask_graphql_auth import create_access_token, create_refresh_token
# Import GraphQL global node id
from graphql_relay.node.node import from_global_id

# Import Models and Types
# users
from app.mod_users.models import Users as UsersModel
from app.mod_users.types import Users as UsersTypes, CreateUserInput
# calendar_periods
from app.mod_calendar_periods.models import Calendar_periods as Calendar_periodsModel  # noqa: E402
from app.mod_calendar_periods.types import Calendar_periods as Calendar_periodsTypes, CreateCalendar_periodsInput  # noqa: E402
# calendar_definitions
from app.mod_calendar_definitions.models import Calendar_definitions as Calendar_definitionsModel  # noqa: E402
from app.mod_calendar_definitions.types import Calendar_definitions as Calendar_definitionsTypes, CreateCalendar_definitionsInput  # noqa: E402
# import new xyz_model and xyz_type, input
# test
from app.mod_test.models import Test as TestModel  # noqa: E402
from app.mod_test.types import Test as TestTypes, CreateTestInput  # noqa: E402
# test
from app.mod_test.models import Test as TestModel  # noqa: E402
from app.mod_test.types import Test as TestTypes, CreateTestInput  # noqa: E402
# test
from app.mod_test.models import Test as TestModel  # noqa: E402
from app.mod_test.types import Test as TestTypes, CreateTestInput  # noqa: E402
# test
from app.mod_test.models import Test as TestModel  # noqa: E402
from app.mod_test.types import Test as TestTypes, CreateTestInput  # noqa: E402
# test
from app.mod_test.models import Test as TestModel  # noqa: E402
from app.mod_test.types import Test as TestTypes, CreateTestInput  # noqa: E402
# test
from app.mod_test.models import Test as TestModel  # noqa: E402
from app.mod_test.types import Test as TestTypes, CreateTestInput  # noqa: E402
# test
from app.mod_test.models import Test as TestModel  # noqa: E402
from app.mod_test.types import Test as TestTypes, CreateTestInput  # noqa: E402
# calendar_periods
from app.mod_calendar_periods.models import Calendar_periods as Calendar_periodsModel  # noqa: E402
from app.mod_calendar_periods.types import Calendar_periods as Calendar_periodsTypes, CreateCalendar_periodsInput  # noqa: E402
# test
from app.mod_test.models import Test as TestModel  # noqa: E402
from app.mod_test.types import Test as TestTypes, CreateTestInput  # noqa: E402



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
            
# calendar_definitions
class Create_Calendar_definitions(graphene.Mutation):
    calendar_definitions = graphene.Field(lambda: Calendar_definitionsTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateCalendar_definitionsInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        calendar_definitions = Calendar_definitionsModel(**data)
        db.session.add(calendar_definitions)
        db.session.commit()
        ok = True
        return Create_Calendar_definitions(calendar_definitions=calendar_definitions, ok=ok)


# new create xyz class

# test
class Create_Test(graphene.Mutation):
    test = graphene.Field(lambda: TestTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateTestInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        test = TestModel(**data)
        db.session.add(test)
        db.session.commit()
        ok = True
        return Create_Test(test=test, ok=ok)

            
# test
class Create_Test(graphene.Mutation):
    test = graphene.Field(lambda: TestTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateTestInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        test = TestModel(**data)
        db.session.add(test)
        db.session.commit()
        ok = True
        return Create_Test(test=test, ok=ok)

            
# test
class Create_Test(graphene.Mutation):
    test = graphene.Field(lambda: TestTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateTestInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        test = TestModel(**data)
        db.session.add(test)
        db.session.commit()
        ok = True
        return Create_Test(test=test, ok=ok)

            
# test
class Create_Test(graphene.Mutation):
    test = graphene.Field(lambda: TestTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateTestInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        test = TestModel(**data)
        db.session.add(test)
        db.session.commit()
        ok = True
        return Create_Test(test=test, ok=ok)

            
# test
class Create_Test(graphene.Mutation):
    test = graphene.Field(lambda: TestTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateTestInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        test = TestModel(**data)
        db.session.add(test)
        db.session.commit()
        ok = True
        return Create_Test(test=test, ok=ok)

            
# test
class Create_Test(graphene.Mutation):
    test = graphene.Field(lambda: TestTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateTestInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        test = TestModel(**data)
        db.session.add(test)
        db.session.commit()
        ok = True
        return Create_Test(test=test, ok=ok)

            
# test
class Create_Test(graphene.Mutation):
    test = graphene.Field(lambda: TestTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateTestInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        test = TestModel(**data)
        db.session.add(test)
        db.session.commit()
        ok = True
        return Create_Test(test=test, ok=ok)

            
# calendar_periods
class Create_Calendar_periods(graphene.Mutation):
    calendar_periods = graphene.Field(lambda: Calendar_periodsTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateCalendar_periodsInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        calendar_periods = Calendar_periodsModel(**data)
        db.session.add(calendar_periods)
        db.session.commit()
        ok = True
        return Create_Calendar_periods(calendar_periods=calendar_periods, ok=ok)

            
# test
class Create_Test(graphene.Mutation):
    test = graphene.Field(lambda: TestTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateTestInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        test = TestModel(**data)
        db.session.add(test)
        db.session.commit()
        ok = True
        return Create_Test(test=test, ok=ok)

            
# calendar_periods
class Create_Calendar_periods(graphene.Mutation):
    calendar_periods = graphene.Field(lambda: Calendar_periodsTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateCalendar_periodsInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        calendar_periods = Calendar_periodsModel(**data)
        db.session.add(calendar_periods)
        db.session.commit()
        ok = True
        return Create_Calendar_periods(calendar_periods=calendar_periods, ok=ok)

            
# calendar_definitions
class Create_Calendar_definitions(graphene.Mutation):
    calendar_definitions = graphene.Field(lambda: Calendar_definitionsTypes)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateCalendar_definitionsInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        calendar_definitions = Calendar_definitionsModel(**data)
        db.session.add(calendar_definitions)
        db.session.commit()
        ok = True
        return Create_Calendar_definitions(calendar_definitions=calendar_definitions, ok=ok)

            
            
class Mutation(graphene.ObjectType):
    createUser = Create_User.Field()
    auth = AuthMutation.Field()
    # calendar_definitions
    createCalendar_definitions = Create_Calendar_definitions.Field()
    # register new createXyz
    # test
    createTest = Create_Test.Field()
    # test
    createTest = Create_Test.Field()
    # test
    createTest = Create_Test.Field()
    # test
    createTest = Create_Test.Field()
    # test
    createTest = Create_Test.Field()
    # test
    createTest = Create_Test.Field()
    # test
    createTest = Create_Test.Field()
    # calendar_periods
    createCalendar_periods = Create_Calendar_periods.Field()
    # test
    createTest = Create_Test.Field()
    # calendar_periods
    createCalendar_periods = Create_Calendar_periods.Field()
    # calendar_definitions
    createCalendar_definitions = Create_Calendar_definitions.Field()

