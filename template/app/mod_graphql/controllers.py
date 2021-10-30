
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import app, db

# Import graph_ql_schema
from app.mod_graphql.schema import schema

# Import GraphQL
from flask_graphql import GraphQLView

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_graphql = Blueprint('graphql', __name__, url_prefix='/graphql')


# Set the route and accepted methods
mod_graphql.add_url_rule(
        '/',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
    )
