import os
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDB:
    client: AsyncIOMotorClient = None

    @classmethod
    def get_database(cls, alias="portofolio"):
        print("Checking MongoDB client:", cls.client)
        if cls.client is None:
            print("MongoDB client is None. Raising exception.")
            raise Exception("You must connect to MongoDB before using it.")
        print("MongoDB client exists. Returning database.")
        return cls.client[alias]


MONGO_URI = "mongodb://localhost:27018/portofolio"  # No Docker
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/") # Docker


async def connect_to_mongo():
    MongoDB.client = AsyncIOMotorClient(MONGO_URI)


async def close_mongo_connection():
    MongoDB.client.close()


def get_database():
    return MongoDB.get_database()
