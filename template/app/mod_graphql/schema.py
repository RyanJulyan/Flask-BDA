import graphene

from app.mod_graphql.query import Query
from app.mod_graphql.mutation import Mutation

from app.mod_users.types import Users as UserType
# import new xyz_types


schema = graphene.Schema(query=Query, mutation=Mutation, types=[
    UserType
    # add new xyz_type_name

])