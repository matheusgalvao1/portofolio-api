import os
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDB:
    client: AsyncIOMotorClient = None

    @classmethod
    def get_database(cls, alias="default"):
        if cls.client is None:
            raise Exception("You must connect to MongoDB before using it.")
        return cls.client[alias]


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")


async def connect_to_mongo():
    MongoDB.client = AsyncIOMotorClient(MONGO_URI)


async def close_mongo_connection():
    MongoDB.client.close()


def get_database():
    return MongoDB.get_database()
