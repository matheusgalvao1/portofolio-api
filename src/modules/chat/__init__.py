from fastapi import APIRouter, Form, HTTPException
from src.models.chat import Chat, Message
from src.modules.chat.bot import get_answer, get_history
import src.db.mongo_chats as mongo_ops

chat_router = APIRouter(tags=["Chat"])


@chat_router.post("/message/")
async def message_endpoint(input: str = Form(...), testMode: bool = Form(False)):
    output = get_answer(input, testMode)
    return output


@chat_router.get("/history/")
async def history_endpoint():
    history = get_history()
    return history


@chat_router.post("/create/", response_model=Chat)
async def create_endpoint():
    chat_id = await mongo_ops.add_new_chat()
    return {"chat_id": chat_id, "messages": []}


@chat_router.post("/add_message/{chat_id}/", response_model=Chat)
async def add_message_to_chat(chat_id: str, message: Message):
    success = await mongo_ops.add_message_to_chat(chat_id, message)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat = await mongo_ops.get_chat(chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@chat_router.get("/get_chat/{chat_id}/", response_model=Chat)
async def get_chat(chat_id: str):
    chat = await mongo_ops.get_chat(chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat
