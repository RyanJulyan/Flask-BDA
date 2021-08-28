
import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField

from app.mod_users.models import Users as UsersModel
from app.mod_users.types import Users as UsersTypes


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    all_users = SQLAlchemyConnectionField(UsersTypes.connection)

    users_by_name = graphene.List(UsersModel, name=graphene.String())

    @staticmethod
    def users_by_name(parent, info, **args):
        q = args.get('name')

        query = UsersModel.get_query(info)

        return query.filter(UsersModel.name.contains(q)).all()