from fastapi import FastAPI, Depends
from src.modules.chat import chat_router
from fastapi.middleware.cors import CORSMiddleware
from src.db.mongo_connect import connect_to_mongo, close_mongo_connection, get_database

app = FastAPI()

app.include_router(chat_router, prefix="/chat")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    print("Connecting to MongoDB...")
    await connect_to_mongo()
    print("Connected to MongoDB")


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


@app.get("/")
async def health_check():
    return {"Status": "OK", "Message": "Access /docs to more information"}
