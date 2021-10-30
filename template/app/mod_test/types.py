
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_test.models import Test


class Test(SQLAlchemyObjectType):
    class Meta:
        model = Test
        interfaces = (graphene.relay.Node,)


class TestAttribute:
    # start new graphene attribute fields
    budget = graphene.Decimal(required=True)
    name = graphene.String(required=True)
    start_date = graphene.Date(required=True)
    end_datetime = graphene.DateTime(required=True)
    test_id = graphene.Int(required=True)    # this line should be removed and replaced with the instanceNames variable
    # end new graphene attribute fields
    # name = graphene.String()


class CreateTestInput(graphene.InputObjectType, TestAttribute):
    pass

