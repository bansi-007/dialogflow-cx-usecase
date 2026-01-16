#!/bin/bash

# Library Assistant - Cloud Functions Deployment Script
# Deploys the webhook handler for DialogFlow CX

set -e

# Configuration
FUNCTION_NAME="library-assistant-webhook"
RUNTIME="python311"
REGION="us-central1"
ENTRY_POINT="handle_webhook"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Library Assistant - Webhook Deployment${NC}"
echo "=============================================="

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

echo -e "${GREEN}Project: ${PROJECT_ID}${NC}"
echo -e "${GREEN}Region: ${REGION}${NC}"
echo ""

# Enable APIs
echo -e "${GREEN}Enabling required APIs...${NC}"
gcloud services enable cloudfunctions.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable run.googleapis.com --quiet

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

# Deploy
echo -e "${GREEN}Deploying Cloud Function...${NC}"
gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --runtime=$RUNTIME \
    --region=$REGION \
    --source=. \
    --entry-point=$ENTRY_POINT \
    --trigger-http \
    --allow-unauthenticated \
    $ENV_VARS \
    --timeout=60s \
    --memory=512MB \
    --max-instances=10

# Get URL
FUNCTION_URL=$(gcloud functions describe $FUNCTION_NAME \
    --gen2 \
    --region=$REGION \
    --format="value(serviceConfig.uri)")

echo ""
echo -e "${GREEN}✓ Deployment successful!${NC}"
echo ""
echo -e "${GREEN}Webhook URL:${NC}"
echo "$FUNCTION_URL"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Copy the webhook URL above"
echo "2. Configure in DialogFlow CX Console"
echo "3. Enable for appropriate intents"
echo ""
echo -e "${GREEN}View logs:${NC}"
echo "gcloud functions logs read $FUNCTION_NAME --gen2 --region=$REGION --limit=50"
