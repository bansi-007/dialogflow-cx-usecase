#!/bin/bash

# DialogFlow CX Webhook Deployment Script
# This script deploys the Cloud Function for DialogFlow CX fulfillment

set -e  # Exit on error

# Configuration
FUNCTION_NAME="dialogflow-webhook"
RUNTIME="python311"
REGION="us-central1"
ENTRY_POINT="handle_webhook"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}DialogFlow CX Webhook Deployment${NC}"
echo "=================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed.${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${YELLOW}Not authenticated. Please run: gcloud auth login${NC}"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}Error: No Google Cloud project set.${NC}"
    echo "Please run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo -e "${GREEN}Project: ${PROJECT_ID}${NC}"
echo -e "${GREEN}Region: ${REGION}${NC}"
echo -e "${GREEN}Function: ${FUNCTION_NAME}${NC}"
echo ""

# Check for API key
if [ -z "$OPENWEATHER_API_KEY" ]; then
    echo -e "${YELLOW}Warning: OPENWEATHER_API_KEY environment variable is not set.${NC}"
    echo "The weather functionality will not work without an API key."
    echo "You can set it with: export OPENWEATHER_API_KEY='your-key-here'"
    echo ""
    read -p "Do you want to continue without the API key? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Enable required APIs
echo -e "${GREEN}Enabling required APIs...${NC}"
gcloud services enable cloudfunctions.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable run.googleapis.com --quiet
gcloud services enable artifactregistry.googleapis.com --quiet

# Build environment variables
ENV_VARS=""
if [ ! -z "$OPENWEATHER_API_KEY" ]; then
    ENV_VARS="--set-env-vars OPENWEATHER_API_KEY=$OPENWEATHER_API_KEY"
fi

# Deploy the function
echo -e "${GREEN}Deploying Cloud Function...${NC}"
echo "This may take a few minutes..."

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
    --memory=256MB

# Get the function URL
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
echo "2. Go to DialogFlow CX Console"
echo "3. Navigate to Fulfillment > Webhooks"
echo "4. Create a new webhook and paste the URL"
echo "5. Enable the webhook for your intents"
echo ""
echo -e "${GREEN}To view logs:${NC}"
echo "gcloud functions logs read $FUNCTION_NAME --gen2 --region=$REGION --limit=50"
