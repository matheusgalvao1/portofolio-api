## Run locally
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## Run on Docker
docker compose up --build
### or
export $(xargs < .env)

docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY -e MONGO_URI_TEMPLATE=$MONGO_URI_TEMPLATE -e MONGO_USER=$MONGO_USER -e MONGO_PASS=$MONGO_PASS api-portofolio-image

## Docker Build and Deploy
docker compose build
docker tag api-portofolio-image mathintosh/portofolioapi:<tag>
docker login // if necessary
docker push mathintosh/portofolioapi:<tag>

## What is missing in Github?
google_key.json
.env
