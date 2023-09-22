from fastapi import APIRouter, Form, HTTPException
from src.models.chat import Chat, Message
from src.modules.chat.bot import get_answer, start_new_chat, finish_chat, exist_instance
import src.db.mongo_chats as mongo_ops

chat_router = APIRouter(tags=["Chat"])


@chat_router.post("/create/")
async def create_endpoint():
    chat_id = await mongo_ops.add_new_chat()
    start_new_chat(chat_id)
    return {"chat_id": chat_id}


@chat_router.post("/finish/{chat_id}/")
async def delete_endpoint(chat_id: str):
    res = finish_chat(chat_id)
    if res:
        return {"message": "Chat finished"}
    else:
        raise HTTPException(status_code=404, detail="Chat not found")


@chat_router.post("/send_message/{chat_id}/", response_model=Chat)
async def add_message_to_chat(chat_id: str, message: str):
    human_message = Message(content=message, author="Human")
    try:
        if not exist_instance(chat_id):
            raise HTTPException(status_code=404, detail="Chat instance does not exist")

        # Add User Message to mongo
        if not await mongo_ops.add_message_to_chat(chat_id, human_message):
            raise HTTPException(status_code=404, detail="Chat could not found in DB")

        # Generate AI response
        ai_content = get_answer(human_message.content, chat_id, False)

        # Add AI Message to mongo
        ai_message = Message(content=ai_content, author="AI")
        if not await mongo_ops.add_message_to_chat(chat_id, ai_message):
            raise HTTPException(status_code=404, detail="Chat not found")

        # Retrieve and return the updated chat
        chat = await mongo_ops.get_chat(chat_id)
        if chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")

        return chat
    except HTTPException as e:
        raise e


@chat_router.get("/get_chat_db/{chat_id}/", response_model=Chat)
async def get_chat_db(chat_id: str):
    try:
        chat = await mongo_ops.get_chat(chat_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Chat not found in DB")
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found in DB")
    return chat


"""
@chat_router.get("/get_chat/{chat_id}/", response_model=Chat)
async def get_chat(chat_id: str):
    inDB = await mongo_ops.get_chat(chat_id)
    if inDB is None:
        raise HTTPException(status_code=404, detail="Chat not found in DB")
    local = get_history(chat_id)
    if local is None:
        raise HTTPException(status_code=404, detail="Chat not found locally")
    if inDB.messages == local:
        return inDB
    else:
        raise HTTPException(
            status_code=500, detail="Chat history mismatch locally and DB"
        )

@chat_router.get("/get_chat_local/{chat_id}/", response_model=Chat)
async def get_chat_local(chat_id: str):
    chat = get_history(chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found locally")
    return chat
"""
