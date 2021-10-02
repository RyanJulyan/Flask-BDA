
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_calendar_definitions.models import Calendar_definitions


class Calendar_definitions(SQLAlchemyObjectType):
    class Meta:
        model = Calendar_definitions
        interfaces = (graphene.relay.Node,)


class Calendar_definitionsAttribute:
    # start new graphene attribute fields
    name = graphene.String(required=True)
    start = graphene.String(required=True)
    end = graphene.String(required=True)
    range_history_periods = graphene.Int(required=True)
    range_future_periods = graphene.Int(required=True)
    freq_period_start_day = graphene.String(required=True)
    freq_normalize = graphene.Boolean(required=True)
    freq_closed = graphene.String(required=True)    # this line should be removed and replaced with the instanceNames variable
    # end new graphene attribute fields
    # name = graphene.String()


class CreateCalendar_definitionsInput(graphene.InputObjectType, Calendar_definitionsAttribute):
    pass

