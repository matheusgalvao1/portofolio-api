# Run locally
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run on Docker
docker compose up --build