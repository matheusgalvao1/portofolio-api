from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    content: str
    author: str


class Chat(BaseModel):
    chat_id: Optional[
        str
    ]  # Will be None when creating a new chat, but should be populated when reading a chat from the database
    messages: List[Message]
