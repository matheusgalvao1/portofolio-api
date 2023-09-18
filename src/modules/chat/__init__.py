from fastapi import APIRouter
from src.modules.chat.bot import get_answer, get_history

chat_router = APIRouter(tags=["Chat"])

@chat_router.get("/message/")
async def message_endpoint(input: str):
    output = get_answer(input)
    return output

@chat_router.get("/history/")
async def history_endpoint():
    history = get_history()
    return history