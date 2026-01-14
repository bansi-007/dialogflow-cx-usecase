# Quick Start Guide

This guide will help you quickly set up and deploy your DialogFlow CX chatbot agent.

## Prerequisites

- Google Cloud Platform account
- `gcloud` CLI installed and configured
- OpenWeatherMap API key (optional, for weather functionality)

## Step-by-Step Setup

### 1. Set Up Google Cloud Project

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable dialogflow.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 2. Get OpenWeatherMap API Key (Optional)

1. Go to https://openweathermap.org/
2. Sign up for a free account
3. Navigate to API keys section
4. Copy your API key
5. Set it as an environment variable:
   ```bash
   export OPENWEATHER_API_KEY="your-api-key-here"
   ```

### 3. Deploy Cloud Function

```bash
cd cloud-functions
./deploy.sh
```

Or manually:
```bash
cd cloud-functions
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

**Note the webhook URL** from the output - you'll need it for DialogFlow CX configuration.

### 4. Create DialogFlow CX Agent

1. Go to https://dialogflow.cloud.google.com/
2. Click "Create Agent"
3. Fill in:
   - **Name**: WeatherAssistant (or your choice)
   - **Default Language**: English
   - **Time Zone**: Your timezone
   - **Location**: us-central1 (or your preferred region)
4. Click "Create"

### 5. Configure Intents

Follow the configurations in `config/intents.md`:

1. Navigate to **Intents** in the left sidebar
2. For each intent (GetWeather, GetGreeting, GetHelp):
   - Click **Create Intent**
   - Add training phrases from the config file
   - Configure parameters
   - Add default responses
   - Enable webhook fulfillment

### 6. Configure Entities

Follow the configurations in `config/entities.md`:

1. Navigate to **Entities** in the left sidebar
2. Create entities:
   - **City** (or use @sys.geo-city)
   - **Name** (or use @sys.person)
   - **WeatherCondition** (optional)

### 7. Set Up Webhook

1. Navigate to **Fulfillment** in the left sidebar
2. Click **Create** under Webhooks
3. Enter your Cloud Function URL (from step 3)
4. Click **Save**
5. Enable webhook for each intent that needs it:
   - GetWeather
   - GetGreeting
   - GetHelp

### 8. Configure Flows and Pages

Follow the configurations in `config/flows-pages.md`:

1. Navigate to **Flows** in the left sidebar
2. Use the default flow or create new flows
3. Create pages:
   - Welcome Page
   - Weather Handling Page
   - Weather Response Page
   - Greeting Page
   - Help Page
4. Configure routes and transitions

### 9. Set Up Event Handlers

Follow the configurations in `config/event-handlers.md`:

1. Navigate to your Flow
2. Add flow-level event handlers:
   - sys.no-match-default
   - sys.no-input-default
   - sys.cancel
3. Add page-level event handlers as needed

### 10. Configure Agent Dialogs

Follow the configurations in `config/agent-dialogs.md`:

1. Navigate to your Flow or Pages
2. Add entry fulfillments for welcome messages
3. Configure form prompts for parameter collection
4. Add contextual help dialogs

### 11. Test Your Agent

1. Click **Test Agent** in the right sidebar
2. Try these test queries:
   - "Hello"
   - "What's the weather in New York?"
   - "Help"
   - "What can you do?"
3. Verify:
   - Intent recognition works
   - Entities are extracted
   - Webhook is called
   - Responses are appropriate

See `docs/testing-guide.md` for comprehensive testing procedures.

## Common Issues and Solutions

### Webhook Not Working

1. **Check Function URL**: Verify the URL is correct in DialogFlow CX
2. **Check Logs**: 
   ```bash
   gcloud functions logs read dialogflow-webhook --gen2 --region=us-central1
   ```
3. **Verify Authentication**: Ensure function allows unauthenticated access
4. **Test Webhook Directly**: Use curl to test the endpoint

### Intent Not Recognized

1. **Add More Training Phrases**: Include variations of user queries
2. **Check Intent Priority**: Ensure correct intent priority settings
3. **Verify Entity Matching**: Check if entities are correctly configured

### API Errors

1. **Check API Key**: Verify OpenWeatherMap API key is set
2. **Check API Quota**: Free tier has rate limits
3. **Verify City Names**: Some city names may need specific formatting

## Next Steps

- Review `docs/setup-guide.md` for detailed setup instructions
- Review `docs/testing-guide.md` for comprehensive testing
- Customize intents, entities, and flows for your use case
- Add more features and integrations

## Resources

- [DialogFlow CX Documentation](https://cloud.google.com/dialogflow/cx/docs)
- [Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [OpenWeatherMap API](https://openweathermap.org/api)

## Support

For issues or questions:
1. Check the documentation files in this project
2. Review Google Cloud Console logs
3. Check DialogFlow CX test agent for debugging
4. Consult official DialogFlow CX documentation
