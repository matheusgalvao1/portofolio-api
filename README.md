## Run locally
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## Run on Docker
docker compose up --build
### or
export $(xargs < .env)

docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY -e MONGO_URI_TEMPLATE=$MONGO_URI_TEMPLATE -e MONGO_USER=$MONGO_USER -e MONGO_PASS=$MONGO_PASS api-portofolio-image

## Azure
### Build image
docker compose build
### Tag image with container registry
docker tag api-portofolio-image portofolioapi.azurecr.io/api-portofolio-image:v1
### Login to registry
az acr login --name portofolioapi
### Push image to registry
docker push portofolioapi.azurecr.io/api-portofolio-image:v1
### Set registry password as cmd variable
export $(xargs < .env)
### Create container
az container create \
--resource-group portfolio \
--name apicontainer \
--image mathintosh/portofolioapi:1.0 \
--registry-login-server docker.io \
--registry-username mathintosh \
--registry-password $DOCKER_TOKEN \
--dns-name-label portofolioapi \
--ports 8000 \
--secrets OPENAI_API_KEY=$OPENAI_API_KEY MONGO_URI_TEMPLATE=$MONGO_URI_TEMPLATE MONGO_USER=$MONGO_USER MONGO_PASS=$MONGO_PASS

### Check logs
az container logs --resource-group portfolio --name apicontainer --follow
### Access docs
portofolioapi.eastus.azurecontainer.io/docs

  

## To build images for linux64 architectures
### You can write this on terminal before
export DOCKER_DEFAULT_PLATFORM=linux/amd64
### Or create the image with buildx
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t mathintosh/portofolioapi:your-tag --push .
### Or add line to docker-compose.yml
platform: linux/amd64