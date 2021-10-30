
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_xyz.models import Xyz


class Xyz(SQLAlchemyObjectType):
    class Meta:
        model = Xyz
        interfaces = (graphene.relay.Node,)


class XyzAttribute:
    # start new graphene attribute fields
    # this line should be removed and replaced with the instanceNames variable
    # end new graphene attribute fields
    # name = graphene.String()


class CreateXyzInput(graphene.InputObjectType, XyzAttribute):
    pass

