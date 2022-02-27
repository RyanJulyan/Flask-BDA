
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_users.models import Users


class Users(SQLAlchemyObjectType):
    class Meta:
        model = Users
        interfaces = (graphene.relay.Node,)


class UsersAttribute:
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    role = graphene.Int(required=True)
    status = graphene.Int(required=True)
    confirmed = graphene.Boolean(required=True)
    confirmed_on = graphene.DateTime()
    session_token = graphene.String()


class CreateUserInput(graphene.InputObjectType, UsersAttribute):
    pass

