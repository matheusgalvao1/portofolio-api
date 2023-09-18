from fastapi import APIRouter
from src.modules.chat.bot import answer

chat_router = APIRouter(tags=["Chat"])

@chat_router.get("/message/")
async def message_endpoint(input: str):
    output = answer(input)
    return output

