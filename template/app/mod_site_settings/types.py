
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_site_settings.models import Site_settings


class Site_settings(SQLAlchemyObjectType):
    class Meta:
        model = Site_settings
        interfaces = (graphene.relay.Node,)


class Site_settingsAttribute:
    # start new graphene attribute fields
    # this line should be removed and replaced with the instanceNames variable
    # end new graphene attribute fields
    # name = graphene.String()


class CreateSite_settingsInput(graphene.InputObjectType, Site_settingsAttribute):
    pass

