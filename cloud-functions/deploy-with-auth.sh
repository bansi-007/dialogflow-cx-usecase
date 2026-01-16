#!/bin/bash

# Library Assistant - Cloud Functions Deployment Script (With Authentication)
# Deploys the webhook handler with authentication enabled

set -e

# Configuration
FUNCTION_NAME="library-assistant-webhook"
RUNTIME="python311"
REGION="us-central1"
ENTRY_POINT="handle_webhook"
SERVICE_ACCOUNT_NAME="dialogflow-cx-webhook"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Library Assistant - Webhook Deployment (With Authentication)${NC}"
echo "=============================================================="

# Check prerequisites
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI not installed${NC}"
    exit 1
fi

# Get project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}Error: No GCP project set${NC}"
    exit 1
fi

PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

echo -e "${GREEN}Project: ${PROJECT_ID}${NC}"
echo -e "${GREEN}Project Number: ${PROJECT_NUMBER}${NC}"
echo -e "${GREEN}Region: ${REGION}${NC}"
echo ""

# Enable APIs
echo -e "${GREEN}Enabling required APIs...${NC}"
gcloud services enable cloudfunctions.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable run.googleapis.com --quiet
gcloud services enable iam.googleapis.com --quiet

# Create service account if it doesn't exist
echo -e "${GREEN}Setting up service account...${NC}"
if ! gcloud iam service-accounts describe ${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com &>/dev/null; then
    echo -e "${YELLOW}Creating service account...${NC}"
    gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
        --display-name="DialogFlow CX Webhook Service Account" \
        --description="Service account for DialogFlow CX to call Cloud Functions" \
        --project=${PROJECT_ID}
else
    echo -e "${GREEN}Service account already exists${NC}"
fi

# Grant Cloud Functions Invoker role to DialogFlow CX default service account
echo -e "${GREEN}Granting permissions...${NC}"
DIALOGFLOW_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud functions add-iam-policy-binding ${FUNCTION_NAME} \
    --gen2 \
    --region=${REGION} \
    --member="serviceAccount:${DIALOGFLOW_SA}" \
    --role="roles/cloudfunctions.invoker" \
    2>/dev/null || echo -e "${YELLOW}Note: Function may not exist yet, permissions will be set after deployment${NC}"

# Build environment variables
ENV_VARS=""
if [ ! -z "$LIBRARY_API_URL" ]; then
    ENV_VARS="$ENV_VARS --set-env-vars LIBRARY_API_URL=$LIBRARY_API_URL"
fi
if [ ! -z "$LIBRARY_API_KEY" ]; then
    ENV_VARS="$ENV_VARS --set-env-vars LIBRARY_API_KEY=$LIBRARY_API_KEY"
fi
if [ ! -z "$USE_MOCK_DATA" ]; then
    ENV_VARS="$ENV_VARS --set-env-vars USE_MOCK_DATA=$USE_MOCK_DATA"
fi

# Deploy with authentication
echo -e "${GREEN}Deploying Cloud Function with authentication...${NC}"
gcloud functions deploy ${FUNCTION_NAME} \
    --gen2 \
    --runtime=${RUNTIME} \
    --region=${REGION} \
    --source=. \
    --entry-point=${ENTRY_POINT} \
    --trigger-http \
    --no-allow-unauthenticated \
    --service-account=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
    ${ENV_VARS} \
    --timeout=60s \
    --memory=512MB \
    --max-instances=10

# Grant permission after deployment
echo -e "${GREEN}Granting DialogFlow CX permission to invoke function...${NC}"
gcloud functions add-iam-policy-binding ${FUNCTION_NAME} \
    --gen2 \
    --region=${REGION} \
    --member="serviceAccount:${DIALOGFLOW_SA}" \
    --role="roles/cloudfunctions.invoker"

# Get URL
FUNCTION_URL=$(gcloud functions describe ${FUNCTION_NAME} \
    --gen2 \
    --region=${REGION} \
    --format="value(serviceConfig.uri)")

echo ""
echo -e "${GREEN}✓ Deployment successful!${NC}"
echo ""
echo -e "${GREEN}Webhook URL:${NC}"
echo "$FUNCTION_URL"
echo ""
echo -e "${YELLOW}Important: Authentication is enabled!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Copy the webhook URL above"
echo "2. In DialogFlow CX Console, go to Fulfillment > Webhooks"
echo "3. Create/edit webhook and paste the URL"
echo "4. Enable 'Enable OIDC Token' in webhook settings"
echo "5. Select service account: ${DIALOGFLOW_SA}"
echo "6. Save the webhook configuration"
echo ""
echo -e "${GREEN}View logs:${NC}"
echo "gcloud functions logs read ${FUNCTION_NAME} --gen2 --region=${REGION} --limit=50"
echo ""
echo -e "${GREEN}Service Account:${NC}"
echo "${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
echo ""
echo -e "${GREEN}DialogFlow CX Service Account:${NC}"
echo "${DIALOGFLOW_SA}"
