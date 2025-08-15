from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
from config import Config

logger = logging.getLogger(__name__)

class MongoDBClient:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(Config.MONGODB_URI)
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client[Config.MONGODB_DATABASE]
            self.collection = self.db[Config.MONGODB_COLLECTION]
            logger.info("Successfully connected to MongoDB")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def insert_document(self, document_data):
        """Insert a document into MongoDB"""
        try:
            result = self.collection.insert_one(document_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting document: {e}")
            raise
    
    def get_document(self, document_id):
        """Get a document by ID"""
        try:
            from bson import ObjectId
            return self.collection.find_one({"_id": ObjectId(document_id)})
        except Exception as e:
            logger.error(f"Error getting document: {e}")
            return None
    
    def get_all_documents(self):
        """Get all documents"""
        try:
            return list(self.collection.find({}, {"_id": 0}))
        except Exception as e:
            logger.error(f"Error getting all documents: {e}")
            return []
    
    def update_document(self, document_id, update_data):
        """Update a document"""
        try:
            from bson import ObjectId
            result = self.collection.update_one(
                {"_id": ObjectId(document_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            return False
    
    def delete_document(self, document_id):
        """Delete a document"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
