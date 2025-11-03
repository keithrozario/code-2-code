#!/bin/bash
echo ${GOOGLE_CLOUD_PROJECT}

set -e
SERVICE_NAME="money-note-api"
REPO_NAME="money-note-repo"

IMAGE_NAME="${GOOGLE_CLOUD_LOCATION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${REPO_NAME}/${SERVICE_NAME}"

echo "--- Creating Artifact Registry Repository (if it doesn't exist) ---"
gcloud artifacts repositories create "${REPO_NAME}" \
  --repository-format=docker \
  --location=${GOOGLE_CLOUD_LOCATION} \
  --description="Docker repository for Money Note API" || echo "Repository ${REPO_NAME} already exists."

echo "--- Building and Pushing Docker Image to Artifact Registry using Cloud Build ---"
gcloud builds submit --tag "${IMAGE_NAME}" .

echo "--- Deploying to Cloud Run ---"
gcloud run deploy "${SERVICE_NAME}" \
  --image="${IMAGE_NAME}" \
  --region="${GOOGLE_CLOUD_LOCATION}" \
  --platform="managed" \
  --allow-unauthenticated \
  --project="${GOOGLE_CLOUD_PROJECT}"

echo "--- Deployment Complete ---"
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --platform managed --region ${GOOGLE_CLOUD_LOCATION} --format 'value(status.url)')
echo "Service URL: ${SERVICE_URL}"
