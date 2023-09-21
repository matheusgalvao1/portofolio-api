from fastapi import FastAPI, Depends
from src.modules.chat import chat_router
from fastapi.middleware.cors import CORSMiddleware
from src.db.mongo_connect import connect_to_mongo, close_mongo_connection, get_database

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


@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


@app.get("/")
async def read_root(db=Depends(get_database)):
    collection = db["example_collection"]
    document = await collection.find_one({"key": "value"})
    return document


@app.get("/")
async def health_check():
    return {"Status": "OK", "Message": "Access /docs to more information"}
