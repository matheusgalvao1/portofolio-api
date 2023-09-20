from fastapi import APIRouter, Form
from src.modules.chat.bot import get_answer, get_history

chat_router = APIRouter(tags=["Chat"])


@chat_router.post("/message/")
async def message_endpoint(input: str = Form(...), testMode: bool = Form(False)):
    output = get_answer(input, testMode)
    return output


@chat_router.get("/history/")
async def history_endpoint():
    history = get_history()
    return history
