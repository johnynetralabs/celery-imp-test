import traceback
from typing import Optional
import threading
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

class MongoConnector:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._client = None
                    cls._instance._database = None
        return cls._instance

    def __init__(self, connection_timeout: int = 30000, server_selection_timeout: int = 30000):
        # This will only execute once due to __new__
        if not hasattr(self, '_initialized'):
            self.connection_timeout = connection_timeout
            self.server_selection_timeout = server_selection_timeout
            self._initialized = True

    async def initialize(self, mongo_url: str, database_name: str) -> None:
        """Initialize connection (call once at startup)"""
        try:
            self._client = AsyncIOMotorClient(
                mongo_url,
                maxPoolSize=20,          # Maximum connections in pool
                minPoolSize=5,           # Minimum connections to maintain
                connectTimeoutMS=self.connection_timeout,
                serverSelectionTimeoutMS=self.server_selection_timeout,
                retryWrites=True,
                retryReads=True,
            )

            await self._client.admin.command("ping")
            self._database = self._client[database_name]
            print("MongoDB connection Created!")

        except Exception as e:
            print(f"❌ MongoDB connection failed: {str(e)}")
            print(traceback.format_exc())
            raise RuntimeError(f"MongoDB connection failed: {str(e)}")

    @property
    def db(self) -> AsyncIOMotorDatabase:
        if self._database is None:
            raise RuntimeError("MongoDB not initialized. Call initialize() first.")
        return self._database

    async def close(self) -> None:
        if self._client:
            self._client.close()
            print("MongoDB connection closed.")


# Singleton instance
mongo_connector = MongoConnector()

# from celery.signals import task_success
# from celery import Celery
# import asyncio
# from motor.motor_asyncio import AsyncIOMotorClient
# from contextlib import asynccontextmanager
# import datetime
# from core import settings

# # MongoDB connection setup (singleton pattern)
# class MongoManager:
#     _client = None
#     _db = None
    
#     @classmethod
#     async def get_db(cls):
#         if cls._client is None:
#             cls._client = AsyncIOMotorClient(settings.MONGODB_URL)
#             cls._db = cls._client[settings.MONGODB_DB]
#         return cls._db

#     @classmethod
#     async def close(cls):
#         if cls._client:
#             cls._client.close()
#             cls._client = None
#             cls._db = None

# @asynccontextmanager
# async def get_mongo_connection():
#     db = await MongoManager.get_db()
#     try:
#         yield db
#     finally:
#         pass  # Connection is managed by MongoManager

