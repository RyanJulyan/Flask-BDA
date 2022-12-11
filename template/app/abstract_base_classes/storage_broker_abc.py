
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class StorageBroker(ABC):
    """ This is where you can add BREAD or CRUD to any of your data sources
         and then you will easily have Browse, Read, Edit, Add, Delete and Search
         functionality for that table.

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

    @abstractmethod
    def browse(self, page: Optional[int]):
        """Return all values (per page) 

        Args:
            page (Optional[int]): The page number for pagination
        """
        pass

    @abstractmethod
    def read(self, id: Any):
        """Return a single record by id

        Args:
            id (Any): The unique identifier that will allow you 
                        to query against
        """
        pass

    @abstractmethod
    def edit(self, id: Any, request: Any):
        """Edit a single record's values

        Args:
            id (Any): The unique identifier that will allow you 
                        to query against
            request (Any): The request you wish to update the record
                        with
        """
        pass

    @abstractmethod
    def add(self, request: Any):
        """Create a single record

        Args:
            request (Any): The request you wish to create a new record
                        with
        """
        pass

    @abstractmethod
    def delete(self, id: Any):
        """Delete a single record

        Args:
            id (Any): The unique identifier that will allow you
                        to query against
        """
        pass

    @abstractmethod
    def search(self, **kwargs: Dict[str, Any]):
        """Search with optional kwargs
        """
        pass

    @abstractmethod
    def relationship_returns(self, **kwargs: Dict[str, Any]):
        """Return any relationship request that the view needs
            with optional kwargs
        """
        pass

    def columns(self):
        """Return the column names
        """
        pass

    def is_singluar(self, entities: list):
        if len(entities) > 1:
            return False
        return True

    def is_empty(self, entities: list):
        if len(entities) == 1:
            return True
        return False
