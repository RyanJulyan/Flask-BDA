
from typing import Any, Dict, Optional

from flask import flash
from sqlalchemy import event, inspect, and_, or_
from sqlalchemy.exc import IntegrityError

from app.abstract_base_classes.storage_broker_abc import StorageBroker

# Import the database object from the main app module
from app import app, db

# Import xyz module models 
from app.mod_xyz.models import Xyz
# Import module models (e.g. User)


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
                Xyz.query
                # relationship join

                .add_columns(
                    Xyz.id,
                    # Xyz query add columns

                    # relationship query add columns

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
                Xyz.query
                # relationship join

                .filter_by(id=id)
                .first_or_404()
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
        data = Xyz.query.get_or_404(id)
        
        # start update request feilds
        # this line should be removed and replaced with the updateFormRequestDefinitions variable
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

        data = Xyz(
            # start new broker data feilds
            # this line should be removed and replaced with the newFormRequestDefinitions variable
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
        data = Xyz.query.get_or_404(id)
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

        context_data = {
            # Relationship context_data
        }

        return context_data

    def columns(self):
        """Return the column names
        """

        return inspect(Xyz)
