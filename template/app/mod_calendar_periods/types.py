
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_calendar_periods.models import Calendar_periods


class Calendar_periods(SQLAlchemyObjectType):
    class Meta:
        model = Calendar_periods
        interfaces = (graphene.relay.Node,)


class Calendar_periodsAttribute:
    # start new graphene attribute fields
    calendar_definition_id = graphene.Int(required=True)
    start_date = graphene.DateTime(required=True)
    end_date = graphene.DateTime(required=True)
    day = graphene.Int(required=True)
    week = graphene.Int(required=True)
    week_day = graphene.String(required=True)
    week_index = graphene.Int(required=True)
    month = graphene.Int(required=True)
    month_index = graphene.Int(required=True)
    quarter = graphene.Int(required=True)
    quarter_index = graphene.Int(required=True)
    year = graphene.Int(required=True)    # this line should be removed and replaced with the instanceNames variable
    # end new graphene attribute fields
    # name = graphene.String()


class CreateCalendar_periodsInput(graphene.InputObjectType, Calendar_periodsAttribute):
    pass

