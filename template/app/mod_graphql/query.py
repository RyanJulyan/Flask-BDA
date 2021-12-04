
import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField

# Import Models and Types
# users
from app.mod_users.models import Users as UsersModel
from app.mod_users.types import Users as UsersTypes
# web_hooks
from app.mod_web_hooks.models import Web_hooks as Web_hooksModel  # noqa: E402
from app.mod_web_hooks.types import Web_hooks as Web_hooksTypes  # noqa: E402
# calendar_definitions
from app.mod_calendar_definitions.models import Calendar_definitions as Calendar_definitionsModel  # noqa: E402
from app.mod_calendar_definitions.types import Calendar_definitions as Calendar_definitionsTypes  # noqa: E402
# calendar_periods
from app.mod_calendar_periods.models import Calendar_periods as Calendar_periodsModel  # noqa: E402
from app.mod_calendar_periods.types import Calendar_periods as Calendar_periodsTypes  # noqa: E402
# import new xyz_model and xyz_type
# statuses
from app.mod_statuses.models import Statuses as StatusesModel  # noqa: E402
from app.mod_statuses.types import Statuses as StatusesTypes  # noqa: E402


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    all_users = SQLAlchemyConnectionField(UsersTypes.connection)
    # web_hooks
    all_web_hooks = SQLAlchemyConnectionField(Web_hooksTypes.connection)
    # calendar_definitions
    all_calendar_definitions = SQLAlchemyConnectionField(Calendar_definitionsTypes.connection)
    # calendar_periods
    all_calendar_periods = SQLAlchemyConnectionField(Calendar_periodsTypes.connection)
    # new xyz_model connection
    # statuses
    all_statuses = SQLAlchemyConnectionField(StatusesTypes.connection)

    users_by_name = graphene.List(UsersModel, name=graphene.String())

    @staticmethod
    def users_by_name(parent, info, **args):
        q = args.get('name')

        query = UsersModel.get_query(info)

        return query.filter(UsersModel.name.contains(q)).all()