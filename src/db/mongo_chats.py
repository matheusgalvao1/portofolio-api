from typing import List, Dict, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from src.models.chat import Chat, Message  # Import the models
import src.db.mongo_connect as db_connect


# Convert a MongoDB chat document to a Chat model
def convert_to_chat_model(chat_doc: Dict) -> Chat:
    return Chat(
        chat_id=str(chat_doc["_id"]),
        messages=[Message(**message) for message in chat_doc["messages"]],
    )


# Function to fetch chats_collection
def get_chats_collection():
    db = db_connect.get_database()
    return db["chats"]


async def add_new_chat() -> str:
    chats_collection = get_chats_collection()
    chat_data = {"messages": []}
    result = await chats_collection.insert_one(chat_data)
    return str(result.inserted_id)


async def add_message_to_chat(chat_id: str, message: Message) -> bool:
    chats_collection = get_chats_collection()
    message_data = message.dict()  # Convert Pydantic model to dictionary
    result = await chats_collection.update_one(
        {"_id": ObjectId(chat_id)}, {"$push": {"messages": message_data}}
    )
    return result.modified_count > 0


async def get_chat(chat_id: str) -> Optional[Chat]:
    chats_collection = get_chats_collection()
    chat_doc = await chats_collection.find_one({"_id": ObjectId(chat_id)})
    if chat_doc:
        return convert_to_chat_model(chat_doc)
    return None


async def get_all_chats() -> List[Chat]:
    chats_collection = get_chats_collection()
    chat_docs = await chats_collection.find().to_list(length=100)
    return [convert_to_chat_model(chat_doc) for chat_doc in chat_docs]


async def delete_chat(chat_id: str) -> bool:
    chats_collection = get_chats_collection()
    result = await chats_collection.delete_one({"_id": ObjectId(chat_id)})
    return result.deleted_count > 0
