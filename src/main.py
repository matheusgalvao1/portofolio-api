from fastapi import FastAPI, Depends
from src.modules.chat import chat_router
from fastapi.middleware.cors import CORSMiddleware
from src.db.mongo_connect import connect_to_mongo, close_mongo_connection, get_database
from google.oauth2 import service_account
from googleapiclient.discovery import build


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


# Global variable to store document content
doc_content = ""


@app.on_event("startup")
async def load_content_from_google_docs():
    global doc_content

    SERVICE_ACCOUNT_FILE = "google_key.json"
    SCOPES = [
        "https://www.googleapis.com/auth/documents.readonly",
        "https://www.googleapis.com/auth/drive",
    ]
    DOCUMENT_ID = "1dv1rNS3zlg8piCFjfBL7vmdJn6vn20U0Pr2So9g9HbU"

    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        docs_service = build("docs", "v1", credentials=credentials)
        document = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return

    # Verify the connection and document retrieval
    if not document or "body" not in document:
        print("Failed to retrieve the document or document format not recognized.")
        return

    # Extracting content
    for element in document.get("body").get("content"):
        if "paragraph" in element:
            for text_run in element.get("paragraph").get("elements"):
                doc_content += text_run.get("textRun").get("content")

    # Write to a file
    filename = "cv.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(doc_content)

    print(f"The content has been written to {filename}")


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


@app.get("/")
async def health_check():
    return {"Status": "OK", "Message": "Access /docs to more information"}
