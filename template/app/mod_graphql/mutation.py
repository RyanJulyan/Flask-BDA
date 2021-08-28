import graphene

from app import db
from app.mod_users.models import Users
from app.mod_users.types import Users, CreateUserInput


# Import GraphQL global node id
from graphql_relay.node.node import from_global_id


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
    user = graphene.Field(lambda: Users)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateUserInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        user = Users(**data)
        db.session.add(user)
        db.session.commit()
        ok = True
        return Create_User(user=user, ok=ok)


class Mutation(graphene.ObjectType):
    createUser = Create_User.Field()