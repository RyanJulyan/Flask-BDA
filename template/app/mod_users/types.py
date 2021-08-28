
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_users.models import Users


class Users(SQLAlchemyObjectType):
    class Meta:
        model = Users
        interfaces = (graphene.relay.Node,)


class UserAttribute:
    name = graphene.String()
    email = graphene.String()
    password = graphene.String()
    role = graphene.Int()
    status = graphene.Int()
    confirmed = graphene.Boolean()
    confirmed_on = graphene.DateTime()
    session_token = graphene.String()


class CreateUserInput(graphene.InputObjectType, UserAttribute):
    pass

