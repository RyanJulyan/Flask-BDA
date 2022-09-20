
from typing import Any, Dict, Optional

from flask import flash
from sqlalchemy import event, inspect, and_, or_
from sqlalchemy.exc import IntegrityError

from app.abstract_base_classes.storage_broker_abc import StorageBroker

# Import the database object from the main app module
from app import app, db

# Import api_keys module models 
from app.mod_api_keys.models import Api_keys
# Import module models (e.g. User)
from app.mod_users.models import Users

class SQLAlchStorageBroker(StorageBroker):
    """ This is where you can add BREAD or CRUD to any of your data sources
         and then you will easily have Browse, Read, Edit, Add, Delete and Search
         functionality for that table.

        This broker will Implement SQLAlchemy as the storage engine

        BROWSE: Return all records (per page)
        READ: Return a single record by id
        EDIT: Edit a single record's values
        ADD: Create a single record
        DELETE: Delete a single record
        SEARCH: Search with optional kwargs

    Args:
        ABC (_type_): Abstract Base Classes (ABCs). Abstract classes are classes 
                     that contain one or more abstract methods. An abstract method 
                     is a method that is declared, but contains no implementation. 
                     Abstract classes cannot be instantiated, and require subclasses 
                     to provide implementations for the abstract methods.
    """

    def browse(self, page: Optional[int]):
        """Return all values (per page) 

        Args:
            page (Optional[int]): The page number for pagination
        """

        data = (
                Api_keys.query
                # relationship join
                .join(Users)
                .add_columns(
                    Api_keys.id,
                    # Api_keys query add columns
                    Api_keys.api_key.label('api_key'),
                                Api_keys.api_key_notes.label('api_key_notes'),
                                Api_keys.valid_from.label('valid_from'),
                                Api_keys.valid_to.label('valid_to'),
            
                    # relationship query add columns
                    Users.name.label('users_name'),
            
                )
                .paginate(page=page, per_page=app.config['ROWS_PER_PAGE'])
            )

        return data

    def read(self, id: Any):
        """Return a single record by id

        Args:
            id (Any): The unique identifier that will allow you 
                        to query against
        """

        data = (
                Api_keys.query
                # relationship join
                .join(Users)
                .get_or_404(id)
            )

        return data

    def edit(self, id: Any, data: Any):
        """Edit a single record's values

        Args:
            id (Any): The unique identifier that will allow you 
                        to query against
            data (Any): The data you wish to update the record
                        with
        """
        data = Api_keys.query.get_or_404(id)
        
        # start update request feilds
        data.api_key = request.form.get('api_key')
        data.api_key_notes = request.form.get('api_key_notes')
        data.created_user_id = request.form.get('created_user_id')
        data.valid_from = fn.convert_to_python_data_type('datetime')(request.form.get('valid_from'))
        data.valid_to = fn.convert_to_python_data_type('datetime')(request.form.get('valid_to'))        # this line should be removed and replaced with the updateFormRequestDefinitions variable
        # end update request feilds
        # data.title = data.get("title", None)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            flash(errorInfo[0], 'error')

        return data

    def add(self, request: Any):
        """Create a single record

        Args:
            request (Any): The request you wish to create a new record
                        with
        """

        data = Api_keys(
            # start new broker data feilds
            api_key = request.form.get('api_key'),
            api_key_notes = request.form.get('api_key_notes'),
            created_user_id = request.form.get('created_user_id'),
            valid_from = fn.convert_to_python_data_type('datetime')(request.form.get('valid_from')),
            valid_to = fn.convert_to_python_data_type('datetime')(request.form.get('valid_to'))
            # end new broker data feilds
            # title=data.get("title", None)
        )
        db.session.add(data)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args

            flash(errorInfo[0], 'error')

        return data

    def delete(self, id: Any):
        """Delete a single record

        Args:
            id (Any): The unique identifier that will allow you 
                        to query against
        """
        data = Api_keys.query.get_or_404(id)
        db.session.delete(data)
        db.session.commit()

    def search(self, **kwargs: Dict[str, Any]):
        """Search with optional kwargs
        """
        pass

    def relationship_returns(self, **kwargs: Dict[str, Any]):
        """Return any relationship request that the view needs
            with optional kwargs
        """
        
        # Relationship returns
    users = Users.query.all()
        context_data = {
            # Relationship context_data

        'users': users        }

        return context_data

    def columns(self):
        """Return the column names
        """

        return inspect(Api_keys)
