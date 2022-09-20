
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_api_keys.models import Api_keys


class Api_keys(SQLAlchemyObjectType):
    class Meta:
        model = Api_keys
        interfaces = (graphene.relay.Node,)


class Api_keysAttribute:
    # start new graphene attribute fields
    api_key = graphene.String()
    api_key_notes = graphene.String()
    created_user_id = graphene.Int()
    valid_from = graphene.DateTime()
    valid_to = graphene.DateTime()    # this line should be removed and replaced with the instanceNames variable
    # end new graphene attribute fields
    # name = graphene.String()


class CreateApi_keysInput(graphene.InputObjectType, Api_keysAttribute):
    pass

