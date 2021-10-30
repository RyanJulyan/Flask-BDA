
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_organisations.models import Organisations


class Organisations(SQLAlchemyObjectType):
    class Meta:
        model = Organisations
        interfaces = (graphene.relay.Node,)


class OrganisationsAttribute:
    # start new graphene attribute fields
    # this line should be removed and replaced with the instanceNames variable
    # end new graphene attribute fields
    # name = graphene.String()


class CreateOrganisationsInput(graphene.InputObjectType, OrganisationsAttribute):
    pass

