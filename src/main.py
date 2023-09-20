from fastapi import FastAPI
from src.modules.chat import chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(chat_router, prefix="/chat")

# CORS configuration
origins = [
    "http://localhost:3000",  # Allow requests from your frontend application
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return {"Status": "OK", "Message": "Access /docs to more information"}
