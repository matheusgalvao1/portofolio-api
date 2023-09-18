from fastapi import FastAPI
from src.modules.chat import chat_router

app = FastAPI()

app.include_router(chat_router, prefix="/chat")

@app.get("/")
async def health_check():
    return {
        "Status":"OK",
        "Message":"Access /docs to more information"    
    }



