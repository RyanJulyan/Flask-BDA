
import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField

# Import Models and Types
# users
from app.mod_users.models import Users as UsersModel
from app.mod_users.types import Users as UsersTypes
# calendar_definitions
from app.mod_calendar_definitions.models import Calendar_definitions as Calendar_definitionsModel  # noqa: E402
from app.mod_calendar_definitions.types import Calendar_definitions as Calendar_definitionsTypes  # noqa: E402
# import new xyz_model and xyz_type


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    all_users = SQLAlchemyConnectionField(UsersTypes.connection)
    # new xyz_model connection
    # calendar_definitions
    all_calendar_definitions = SQLAlchemyConnectionField(Calendar_definitionsTypes.connection)

    users_by_name = graphene.List(UsersModel, name=graphene.String())

    @staticmethod
    def users_by_name(parent, info, **args):
        q = args.get('name')

        query = UsersModel.get_query(info)

        return query.filter(UsersModel.name.contains(q)).all()