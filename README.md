# DialogFlow CX Chatbot Agent

A comprehensive DialogFlow CX chatbot implementation with webhook fulfillment, flows, pages, and event handling.

## Project Structure

```
DialogFlow/
├── README.md                          # This file
├── cloud-functions/                   # Cloud Functions for webhook fulfillment
│   ├── main.py                        # Python webhook handler
│   ├── requirements.txt               # Python dependencies
│   └── .gcloudignore                  # Files to ignore in deployment
├── config/                            # DialogFlow CX configuration examples
│   ├── intents.md                     # Intent definitions
│   ├── entities.md                    # Entity definitions
│   ├── flows-pages.md                 # Flow and page structure
│   └── event-handlers.md              # Event handler configurations
└── docs/                              # Documentation
    ├── setup-guide.md                 # Step-by-step setup instructions
    └── testing-guide.md               # Testing procedures
```

## Features

- ✅ Multiple intents with training phrases
- ✅ Entity extraction with synonyms
- ✅ Parameter extraction from user utterances
- ✅ Webhook fulfillment using Cloud Functions
- ✅ External API integration (OpenWeatherMap)
- ✅ Conversation flows and pages
- ✅ Agent dialogs
- ✅ Event handlers

## Quick Start

1. **Prerequisites**
   - Google Cloud Platform account
   - DialogFlow CX API enabled
   - OpenWeatherMap API key (optional, for weather intent)

2. **Setup Instructions**
   See [docs/setup-guide.md](docs/setup-guide.md) for detailed setup steps.

3. **Deploy Cloud Functions**
   ```bash
   cd cloud-functions
   gcloud functions deploy dialogflow-webhook \
     --gen2 \
     --runtime=python311 \
     --region=us-central1 \
     --source=. \
     --entry-point=handle_webhook \
     --trigger-http \
     --allow-unauthenticated
   ```

4. **Configure DialogFlow CX**
   - Follow the configuration examples in the `config/` directory
   - Set up intents, entities, flows, and pages in the DialogFlow CX console

## Testing

See [docs/testing-guide.md](docs/testing-guide.md) for comprehensive testing procedures.

## API Integration

This project uses the OpenWeatherMap API for weather-related queries. You'll need to:
1. Sign up at https://openweathermap.org/
2. Get your API key
3. Set it as an environment variable in Cloud Functions
