import logging
from typing import List, Union, Dict

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.model import Todo


class Todos:
    _logger = logging.getLogger(__name__)
    _client: MongoClient
    _collection_name: str
    _database_name: str
    _database: Database
    _collection: Collection

    def __init__(self, database: str, collection: str, mongo_client: MongoClient):
        self._client = mongo_client
        self._collection_name = collection
        self._database_name = database
        self._database = mongo_client.get_database(database)
        self._collection = self._database.get_collection(self._collection_name)

    def fetch_by_id(self, identifier: str) -> Todo:
        result = self._collection.find_one({'_id': ObjectId(identifier)})
        return Todo(**result)

    def fetch_all(self) -> List[Todo]:
        result = self._collection.find()
        return [Todo(**x) for x in result]

    def save(self, todo: Union[Todo, Dict]) -> str:
        result = self._collection.insert_one(todo)
        return str(result.inserted_id)

    def save_all(self, todos: List[Union[Todo, Dict]]) -> List[str]:
        result = self._collection.insert_many(todos)
        return [str(x) for x in result.inserted_ids]

    def remove_by_id(self, identifier: str) -> bool:
        delete_result = self._collection.delete_one({'_id': ObjectId(identifier)})
        return delete_result.deleted_count == 1

    def clear(self):
        self._collection.delete_many({})
