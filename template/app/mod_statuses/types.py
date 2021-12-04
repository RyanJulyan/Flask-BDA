
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_statuses.models import Statuses


class Statuses(SQLAlchemyObjectType):
    class Meta:
        model = Statuses
        interfaces = (graphene.relay.Node,)


class StatusesAttribute:
    # start new graphene attribute fields
    status_key = graphene.String()
    status_display_name = graphene.String()
    status_description = graphene.String()
    status_group = graphene.String()
    key_value = graphene.String()    # this line should be removed and replaced with the instanceNames variable
    # end new graphene attribute fields
    # name = graphene.String()


class CreateStatusesInput(graphene.InputObjectType, StatusesAttribute):
    pass

