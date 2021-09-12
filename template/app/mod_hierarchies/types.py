
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_hierarchies.models import Hierarchies


class Hierarchies(SQLAlchemyObjectType):
    class Meta:
        model = Hierarchies
        interfaces = (graphene.relay.Node,)


class HierarchiesAttribute:
    # start new graphene attribute fields
    # this line should be removed and replaced with the instanceNames variable
    # end new graphene attribute fields
    # name = graphene.String()


class CreateHierarchiesInput(graphene.InputObjectType, HierarchiesAttribute):
    pass

