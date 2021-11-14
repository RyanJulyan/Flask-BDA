
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.mod_web_hooks.models import Web_hooks


class Web_hooks(SQLAlchemyObjectType):
    class Meta:
        model = Web_hooks
        interfaces = (graphene.relay.Node,)


class Web_hooksAttribute:
    # start new graphene attribute fields
    webhook_name = graphene.String(required=True)
    run_in_module_name = graphene.String(required=True)
    run_before_insert = graphene.Boolean(required=True)
    run_after_insert = graphene.Boolean(required=True)
    run_before_update = graphene.Boolean(required=True)
    run_after_update = graphene.Boolean(required=True)
    run_before_delete = graphene.Boolean(required=True)
    run_after_delete = graphene.Boolean(required=True)
    method = graphene.String(required=True)
    data_type = graphene.String(required=True)
    api_endpoint = graphene.String(required=True)
    api_headers = graphene.String(required=False)
    api_params = graphene.String(required=False)
    active_flag = graphene.Boolean(required=True)    # this line should be removed and replaced with the instanceNames variable
    # end new graphene attribute fields
    # name = graphene.String()


class CreateWeb_hooksInput(graphene.InputObjectType, Web_hooksAttribute):
    pass

