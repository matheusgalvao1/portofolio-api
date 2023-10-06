import os
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus


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


mongo_user = os.getenv("MONGO_USER")
mongo_pass = os.getenv("MONGO_PASS")
mongo_uri_template = os.getenv("MONGO_URI_TEMPLATE")

# Error handling: ensure the environment variables were found
if not all([mongo_user, mongo_pass, mongo_uri_template]):
    raise EnvironmentError(
        "Missing one or more required environment variables (MONGO_USER, MONGO_PASS, MONGO_URI_TEMPLATE)"
    )

escaped_user = quote_plus(mongo_user)
escaped_pass = quote_plus(mongo_pass)
MONGO_URI = mongo_uri_template.format(escaped_user, escaped_pass)
print("MONGO_URI:", MONGO_URI)
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27018/")


async def connect_to_mongo():
    MongoDB.client = AsyncIOMotorClient(MONGO_URI)


async def close_mongo_connection():
    MongoDB.client.close()


def get_database():
    return MongoDB.get_database()
