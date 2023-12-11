from typing import Literal
from pymongo import MongoClient

class SyncPyMongoORM:
    def __init__(self, connection_string: str, database_structures: dict[str, list[str]]) -> None:
        """
        Initializes a SyncPyMongoORM instance with the provided MongoDB connection string and a list of database names.

        Args:
            connection_string (str): MongoDB connection string, including necessary credentials and host information.
            databases (dict): A dictionairy of databases with their respective collections. Sets each passed database and collection as instance attributes.

        Example:
            ```python
            connection_string = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/test?retryWrites=true&w=majority"
            databases = ["mydatabase1", "mydatabase2"]
            sync_mongo_orm = SyncPyMongoORM(connection_string, databases)
            ```
        """
        self._client = MongoClient(connection_string)
        
        for database, database_collections in database_structures.items():
            db_attr = setattr(self, database, self._client[database])
            
            for collection in database_collections:
                setattr(self, collection, db_attr[collection])
            
    def add(self, type: Literal["database", "database.collection"], name: str) -> None:
        if type == 'database':
            setattr(self, name, self._client[name])

        else:
            split = name.split('.')
            database, collection = split

            if not hasattr(self, database):
                setattr(self, database, self._client[database])
                
            setattr(self, collection, getattr(self, database)[collection])
    
    
