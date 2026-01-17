#!/bin/bash

# Deploy demo.html to Google Cloud Storage for public access
# This creates a publicly accessible URL for your demo

set -e

echo "======================================"
echo "Library Assistant - Demo Deployment"
echo "======================================"
echo ""

PROJECT_ID="dialogflow-480615"
BUCKET_NAME="${PROJECT_ID}-demo"
REGION="us-central1"

echo "Project: $PROJECT_ID"
echo "Bucket: $BUCKET_NAME"
echo ""

# Create bucket if it doesn't exist
echo "Creating storage bucket..."
gsutil mb -p $PROJECT_ID -c STANDARD -l $REGION gs://$BUCKET_NAME/ 2>/dev/null || echo "Bucket already exists"

# Make bucket public for website hosting
echo "Configuring bucket for public access..."
gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME

# Set bucket as website
echo "Enabling website configuration..."
gsutil web set -m demo.html gs://$BUCKET_NAME

# Upload demo.html
echo "Uploading demo.html..."
gsutil cp demo.html gs://$BUCKET_NAME/demo.html

# Set cache control
gsutil setmeta -h "Cache-Control:public, max-age=300" gs://$BUCKET_NAME/demo.html

echo ""
echo "✓ Deployment successful!"
echo ""
echo "Public URL:"
echo "https://storage.googleapis.com/$BUCKET_NAME/demo.html"
echo ""
echo "Alternative URL:"
echo "https://$BUCKET_NAME.storage.googleapis.com/demo.html"
echo ""
