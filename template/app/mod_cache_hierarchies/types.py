
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_cache_hierarchies.models import Cache_hierarchies


class Cache_hierarchies(SQLAlchemyObjectType):
    class Meta:
        model = Cache_hierarchies
        interfaces = (graphene.relay.Node,)


class Cache_hierarchiesAttribute:
    # start new graphene attribute fields
    # this line should be removed and replaced with the instanceNames variable
    # end new graphene attribute fields
    # name = graphene.String()


class CreateCache_hierarchiesInput(graphene.InputObjectType, Cache_hierarchiesAttribute):
    pass

