# DialogFlow CX Setup Guide

## Step 1: Create a New Agent

1. **Log in to DialogFlow CX Console**
   - Go to https://dialogflow.cloud.google.com/
   - Select or create a Google Cloud Project

2. **Create New Agent**
   - Click "Create Agent"
   - Agent Name: `WeatherAssistant` (or your preferred name)
   - Default Language: English (en)
   - Time Zone: Select your timezone
   - Location: Choose a region (e.g., us-central1)
   - Click "Create"

## Step 2: Enable Required APIs

1. **Enable DialogFlow CX API**
   ```bash
   gcloud services enable dialogflow.googleapis.com
   ```

2. **Enable Cloud Functions API**
   ```bash
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

## Step 3: Set Up Cloud Functions

1. **Navigate to Cloud Functions**
   ```bash
   cd cloud-functions
   ```

2. **Set Environment Variables**
   ```bash
   export OPENWEATHER_API_KEY="your-api-key-here"
   ```

3. **Deploy the Function**
   ```bash
   gcloud functions deploy dialogflow-webhook \
     --gen2 \
     --runtime=python311 \
     --region=us-central1 \
     --source=. \
     --entry-point=handle_webhook \
     --trigger-http \
     --allow-unauthenticated \
     --set-env-vars OPENWEATHER_API_KEY=$OPENWEATHER_API_KEY
   ```

4. **Get the Webhook URL**
   After deployment, note the `uri` from the output. It will look like:
   ```
   https://us-central1-PROJECT_ID.cloudfunctions.net/dialogflow-webhook
   ```

## Step 4: Configure Intents

Follow the intent definitions in `config/intents.md` and create them in the DialogFlow CX console:

1. Navigate to **Intents** in the left sidebar
2. Click **Create Intent** for each intent
3. Add training phrases and responses as specified
4. Configure parameters for each intent

## Step 5: Configure Entities

1. Navigate to **Entities** in the left sidebar
2. Create entities as defined in `config/entities.md`
3. Add synonyms and variations

## Step 6: Create Flows and Pages

1. Navigate to **Flows** in the left sidebar
2. Use the default flow or create new flows
3. Create pages as defined in `config/flows-pages.md`
4. Configure transitions between pages

## Step 7: Configure Webhook

1. Navigate to **Fulfillment** in the left sidebar
2. Click **Create** under Webhooks
3. Enter your Cloud Function URL
4. Enable the webhook for specific intents

## Step 8: Set Up Event Handlers

1. Navigate to **Flows** > Select your flow
2. Click on the flow's settings
3. Add event handlers as defined in `config/event-handlers.md`

## Step 9: Configure Agent Dialogs

1. Navigate to **Flows** > Select your flow
2. Add agent dialogs at the flow or page level
3. Configure welcome messages and prompts

## Step 10: Test Your Agent

1. Use the **Test Agent** panel in the DialogFlow CX console
2. Try various user utterances
3. Verify intent recognition, entity extraction, and webhook responses
4. See `docs/testing-guide.md` for detailed testing procedures
