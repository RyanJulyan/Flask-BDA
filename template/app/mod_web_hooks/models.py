
# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Import aggregated functionality 
from sqlalchemy_utils import aggregated


# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), index=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), index=True)
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)

    # @aggregated('web_hooks_count', db.Column(db.Integer))
    # def web_hooks_count(self):
    #     return db.func.count('1')


# Define a Web_hooks model
class Web_hooks(Base):
    __tablename__ = 'web_hooks'
    # start new field definitions
    webhook_name = db.Column(db.String(256), nullable=False, default=False, unique=False, index=True)
    run_in_module_name = db.Column(db.String(256), nullable=False, default=False, unique=False, index=True)
    run_before_insert = db.Column(db.Boolean, nullable=False, default=0, unique=False, index=True)
    run_after_insert = db.Column(db.Boolean, nullable=False, default=1, unique=False, index=True)
    run_before_update = db.Column(db.Boolean, nullable=False, default=0, unique=False, index=True)
    run_after_update = db.Column(db.Boolean, nullable=False, default=1, unique=False, index=True)
    run_before_delete = db.Column(db.Boolean, nullable=False, default=0, unique=False, index=True)
    run_after_delete = db.Column(db.Boolean, nullable=False, default=1, unique=False, index=True)
    method = db.Column(db.String(256), nullable=False, default='get', unique=False, index=True)
    data_type = db.Column(db.String(256), nullable=False, default='json', unique=False, index=True)
    api_endpoint = db.Column(db.Text, nullable=False, default=False, unique=False, index=False)
    api_headers = db.Column(db.Text, nullable=True, default='[]', unique=False, index=False)
    api_params = db.Column(db.Text, nullable=True, default='[]', unique=False, index=False)
    active_flag = db.Column(db.Boolean, nullable=False, default=1, unique=False, index=True)    # this line should be removed and replaced with the columns variable
    # end new field definitions
    # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

    # New instance instantiation procedure
    def __init__(self, webhook_name, run_in_module_name, run_before_insert, run_after_insert, run_before_update, run_after_update, run_before_delete, run_after_delete, method, data_type, api_endpoint, api_headers, api_params, active_flag):  # ,example_field):
        # start new instance fields
        self.webhook_name = webhook_name
        self.run_in_module_name = run_in_module_name
        self.run_before_insert = run_before_insert
        self.run_after_insert = run_after_insert
        self.run_before_update = run_before_update
        self.run_after_update = run_after_update
        self.run_before_delete = run_before_delete
        self.run_after_delete = run_after_delete
        self.method = method
        self.data_type = data_type
        self.api_endpoint = api_endpoint
        self.api_headers = api_headers
        self.api_params = api_params
        self.active_flag = active_flag
        # end new instance fields
        # self.example_field = example_field

    def __repr__(self):
        # Set model quick lookup
        return '<Web_hooks %r>' % (self.id)
