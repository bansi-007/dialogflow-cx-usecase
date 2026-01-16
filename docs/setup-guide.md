# Library Assistant - Complete Setup Guide

## Overview

This guide provides step-by-step instructions for setting up the professional Library Assistant using DialogFlow CX with all advanced features.

## Prerequisites

- Google Cloud Platform account with billing enabled
- DialogFlow CX API enabled
- Cloud Functions API enabled
- Basic familiarity with DialogFlow CX console
- Library system API access (or use mock data for testing)

## Step 1: Google Cloud Setup

### 1.1 Create or Select Project

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Or create a new project
gcloud projects create library-assistant-project --name="Library Assistant"
gcloud config set project library-assistant-project
```

### 1.2 Enable Required APIs

```bash
# Enable DialogFlow CX API
gcloud services enable dialogflow.googleapis.com

# Enable Cloud Functions API
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### 1.3 Set Up Authentication

```bash
# Authenticate if needed
gcloud auth login

# Set application default credentials
gcloud auth application-default login
```

## Step 2: Deploy Cloud Functions

### 2.1 Configure Environment Variables

```bash
# Set library API configuration (optional - use mock data if not available)
export LIBRARY_API_URL="https://api.library.example.com"
export LIBRARY_API_KEY="your-api-key"

# Or use mock data for testing
export USE_MOCK_DATA="true"
```

### 2.2 Deploy Webhook

```bash
cd cloud-functions
./deploy.sh
```

Or manually:

```bash
cd cloud-functions
gcloud functions deploy library-assistant-webhook \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=handle_webhook \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars USE_MOCK_DATA=true \
  --timeout=60s \
  --memory=512MB
```

### 2.3 Get Webhook URL

After deployment, note the webhook URL:

```bash
gcloud functions describe library-assistant-webhook \
  --gen2 \
  --region=us-central1 \
  --format="value(serviceConfig.uri)"
```

**Save this URL** - you'll need it for DialogFlow CX configuration.

## Step 3: Create DialogFlow CX Agent

### 3.1 Create Agent

1. Go to [DialogFlow CX Console](https://dialogflow.cloud.google.com/)
2. Click **"Create Agent"**
3. Fill in:
   - **Agent Name**: Library Assistant
   - **Default Language**: English (en)
   - **Time Zone**: Your timezone
   - **Location**: us-central1 (or your preferred region)
   - **Google Project**: Select your project
4. Click **"Create"**

### 3.2 Configure Agent Settings

1. Navigate to **Agent Settings**
2. Configure:
   - **Speech Settings**: Enable speech recognition
   - **Advanced Settings**: Enable multi-turn conversations
   - **Security**: Configure as needed

## Step 4: Configure Authentication (Optional but Recommended)

DialogFlow CX can call your Cloud Function with or without authentication. For production, authentication is recommended.

### Option 1: Unauthenticated Access (Easier, Less Secure)

**Current Setup**: The deployment script uses `--allow-unauthenticated`, which means anyone with the URL can call the function.

**When to Use**: Development, testing, or if you have other security measures in place.

**Configuration**: No additional steps needed - the function is already configured for unauthenticated access.

### Option 2: Authenticated Access (Recommended for Production)

**Benefits**: More secure, only DialogFlow CX can call your function.

**Setup Steps**:

#### 4.1 Create Service Account for DialogFlow CX

```bash
# Create service account
gcloud iam service-accounts create dialogflow-cx-webhook \
  --display-name="DialogFlow CX Webhook Service Account" \
  --description="Service account for DialogFlow CX to call Cloud Functions"

# Grant necessary permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:dialogflow-cx-webhook@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.invoker"
```

#### 4.2 Redeploy Function with Authentication

**Option A: Require Authentication (Remove --allow-unauthenticated)**

```bash
cd cloud-functions

# Redeploy without --allow-unauthenticated flag
gcloud functions deploy library-assistant-webhook \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=handle_webhook \
  --trigger-http \
  --no-allow-unauthenticated \
  --set-env-vars USE_MOCK_DATA=true \
  --timeout=60s \
  --memory=512MB
```

**Option B: Use Service Account (More Secure)**

```bash
# Deploy with service account
gcloud functions deploy library-assistant-webhook \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=handle_webhook \
  --trigger-http \
  --no-allow-unauthenticated \
  --service-account=dialogflow-cx-webhook@PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars USE_MOCK_DATA=true \
  --timeout=60s \
  --memory=512MB
```

#### 4.3 Grant DialogFlow CX Permission to Invoke Function

```bash
# Grant DialogFlow CX service account permission to invoke the function
gcloud functions add-iam-policy-binding library-assistant-webhook \
  --gen2 \
  --region=us-central1 \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/cloudfunctions.invoker"
```

**Note**: Replace `PROJECT_NUMBER` with your actual project number. You can find it with:
```bash
gcloud projects describe PROJECT_ID --format="value(projectNumber)"
```

#### 4.4 Configure DialogFlow CX to Use OIDC Token

When configuring the webhook in DialogFlow CX (Step 5), you'll need to:

1. Navigate to **Fulfillment** > **Webhooks**
2. Create or edit your webhook
3. Enable **"Enable OIDC Token"**
4. Select **"Service Account"** and choose the service account you created
5. Or use **"Compute Engine default service account"** if using the default

**Important**: DialogFlow CX will automatically include the OIDC token in requests when this is enabled.

### Option 3: API Key Authentication (Alternative)

If you prefer API key authentication:

```bash
# Create API key
gcloud alpha services api-keys create \
  --display-name="Library Assistant API Key"

# Restrict API key to Cloud Functions
gcloud alpha services api-keys update API_KEY_ID \
  --api-target=service=cloudfunctions.googleapis.com
```

Then modify your Cloud Function to validate the API key in the request headers.

### Recommendation

- **Development/Testing**: Use Option 1 (Unauthenticated)
- **Production**: Use Option 2 (Authenticated with Service Account)

---

## Step 5: Configure Webhook

1. Navigate to **Fulfillment** in the left sidebar
2. Click **"Create"** under Webhooks
3. Enter:
   - **Display Name**: library-assistant-webhook
   - **URL**: Paste your Cloud Function URL from Step 2.3
   - **Method**: POST
4. **If using authentication (Option 2)**:
   - Enable **"Enable OIDC Token"**
   - Select the appropriate service account
5. Click **"Save"**

### Testing Webhook Authentication

After configuration, test the webhook:

1. Go to **Test Agent** in DialogFlow CX
2. Try an intent that uses the webhook
3. Check the logs if it fails:
   ```bash
   gcloud functions logs read library-assistant-webhook \
     --gen2 \
     --region=us-central1 \
     --limit=20
   ```

**Common Authentication Issues**:
- **403 Forbidden**: Service account doesn't have `cloudfunctions.invoker` role
- **401 Unauthorized**: OIDC token not enabled in DialogFlow CX webhook config
- **Function not found**: Check function name and region match

## Step 6: Create Entities

Follow the configurations in `config/entities/`:

### 5.1 Book Entities

1. Navigate to **Entities**
2. Create entities as specified in `config/entities/book-entities.md`:
   - **BookTitle**: With synonyms and fuzzy matching
   - **AuthorName**: With common author names
   - **Genre**: With genre categories
   - **ISBN**: Using @sys.number-sequence

### 5.2 Account Entities

Create entities from `config/entities/account-entities.md`:
   - **PaymentMethod**: Credit card, debit card, etc.
   - **TransactionID**: Using @sys.number

### 5.3 Reservation Entities

Create entities from `config/entities/reservation-entities.md`:
   - **RoomNumber**: Study room identifiers
   - **EquipmentType**: Laptop, projector, etc.
   - **Duration**: Using @sys.duration

## Step 7: Create Intents

Follow the configurations in `config/intents/`:

### 6.1 Book Search Intents

1. Navigate to **Intents**
2. Create intents from `config/intents/book-search-intents.md`:
   - **SearchBooks**: With training phrases
   - **FindBook**: Alternative search intent
   - **BrowseBooks**: Browse by category
   - **GetRecommendations**: Personalized recommendations
   - **PlaceHold**: Place holds on books

### 6.2 Account Intents

Create intents from `config/intents/account-intents.md`:
   - **ViewCheckouts**: View borrowed books
   - **RenewBook**: Renew books
   - **ViewHolds**: View holds
   - **ViewFines**: View fines
   - **PayFines**: Pay fines

### 6.3 Reservation Intents

Create intents from `config/intents/reservation-intents.md`:
   - **BookRoom**: Book study rooms
   - **ReserveEquipment**: Reserve equipment
   - **RegisterForEvent**: Register for events

### 6.4 General Intents

Create intents from `config/intents/general-intents.md`:
   - **Greeting**: User greetings
   - **GetHelp**: Help requests
   - **FAQ**: FAQ queries

**For each intent**:
- Add training phrases (10-20 variations)
- Configure parameters
- Enable webhook fulfillment where needed
- Set default responses

## Step 8: Create Flows

### 7.1 Main Navigation Flow

1. Navigate to **Flows**
2. Use the default flow or create **"Main Navigation Flow"**
3. Follow `config/flows/main-navigation.md`:
   - Create **Start Page** with welcome message
   - Create **Intent Router Page** for routing
   - Configure routes to other flows
   - Add event handlers

### 7.2 Book Search Flow

1. Create new flow: **"Book Search Flow"**
2. Follow `config/flows/book-search.md`:
   - Create pages: Search Entry, Search Form, Results, Details, Hold Placement
   - Configure forms for parameter collection
   - Set up routes and transitions
   - Enable webhook for data retrieval

### 7.3 Account Management Flow

1. Create new flow: **"Account Management Flow"**
2. Follow `config/flows/account-management.md`:
   - Create pages: Account Entry, Checkouts, Renewal, Holds, Fines, Payment
   - Configure authentication checks
   - Set up account operations
   - Enable webhook for account data

### 7.4 Reservations Flow

1. Create new flow: **"Reservations Flow"**
2. Follow `config/flows/reservations.md`:
   - Create pages for room booking, equipment reservation, event registration
   - Configure date/time parameter collection
   - Set up availability checks
   - Enable webhook for bookings

### 7.5 Help & FAQ Flow

1. Create new flow: **"Help & FAQ Flow"**
2. Follow `config/flows/help-faq.md`:
   - Create pages for FAQ handling
   - Configure knowledge connector (see Step 8)
   - Set up help topics
   - Enable human agent escalation

### 7.6 Authentication Flow

1. Create new flow: **"Authentication Flow"**
2. Configure login pages:
   - Login prompt page
   - Verification page
   - Session management

## Step 9: Configure Knowledge Connector

### 8.1 Create Knowledge Base

1. Navigate to **Knowledge** in DialogFlow CX
2. Click **"Create Knowledge Base"**
3. Configure:
   - **Name**: Library FAQ Knowledge Base
   - **Type**: FAQ or Documents
4. Add documents or FAQ entries:
   - Library hours
   - Borrowing policies
   - Services information
   - Contact information

### 8.2 Connect to Help Flow

1. Navigate to **Help & FAQ Flow**
2. Configure knowledge connector:
   - Enable knowledge connector
   - Select knowledge base
   - Set confidence threshold
   - Configure fallback responses

## Step 10: Configure Rich Responses

Follow `config/advanced-features/rich-responses.md`:

### 9.1 Cards

Configure card responses for:
- Book information
- Account summaries
- Booking confirmations

### 9.2 Lists

Configure list responses for:
- Search results
- Checkouts
- Available rooms

### 9.3 Quick Replies

Add quick reply buttons for:
- Common actions
- Navigation shortcuts
- Confirmation options

## Step 11: Set Up Event Handlers

### 10.1 Flow-Level Handlers

For each flow, add:
- **sys.welcome**: Welcome messages
- **sys.no-match-default**: Fallback handling
- **sys.no-input-default**: No input handling
- **sys.cancel**: Cancellation handling

### 10.2 Page-Level Handlers

Add handlers for:
- Parameter validation errors
- Form completion errors
- Webhook failures

## Step 12: Configure Advanced Features

### 11.1 Conditional Routing

Set up conditional logic:
- Route based on user authentication
- Route based on account status
- Route based on availability

### 11.2 State Management

Configure session variables:
- User ID
- Authentication status
- Current context
- Search history

### 11.3 Context Management

Set up context:
- Preserve context across flows
- Pass parameters between pages
- Maintain conversation state

## Step 13: Testing

### 12.1 Test Agent Panel

1. Open **Test Agent** panel in DialogFlow CX
2. Test each flow:
   - Main Navigation
   - Book Search
   - Account Management
   - Reservations
   - Help & FAQ

### 12.2 Test Scenarios

Follow `docs/testing-guide.md` for comprehensive testing:
- Intent recognition
- Entity extraction
- Parameter collection
- Webhook responses
- Flow navigation
- Error handling

### 12.3 Check Logs

```bash
# View Cloud Functions logs
gcloud functions logs read library-assistant-webhook \
  --gen2 \
  --region=us-central1 \
  --limit=50

# View DialogFlow CX logs
# In DialogFlow CX Console > Logs
```

## Step 14: Iteration and Refinement

### 13.1 Add Training Phrases

Based on test results:
- Add more training phrases
- Improve intent recognition
- Handle edge cases

### 13.2 Refine Responses

- Improve response messages
- Add more rich responses
- Enhance error messages

### 13.3 Optimize Flows

- Simplify complex flows
- Improve navigation
- Reduce user friction

## Troubleshooting

### Common Issues

1. **Webhook Not Working**
   - Check webhook URL is correct
   - Verify Cloud Function is deployed
   - Check function logs for errors
   - Verify authentication settings

2. **Intent Not Recognized**
   - Add more training phrases
   - Check intent priority
   - Verify entity matching

3. **Parameters Not Extracted**
   - Check entity configuration
   - Verify parameter names match
   - Test entity extraction

4. **Flow Navigation Issues**
   - Check route conditions
   - Verify page transitions
   - Check context preservation

## Next Steps

1. **Production Deployment**
   - Set up production environment
   - Configure production APIs
   - Set up monitoring

2. **Analytics**
   - Enable conversation analytics
   - Track user interactions
   - Monitor performance

3. **Enhancements**
   - Add more features
   - Integrate additional services
   - Improve user experience

## Resources

- [DialogFlow CX Documentation](https://cloud.google.com/dialogflow/cx/docs)
- [Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- Configuration files in `config/` directory
- Architecture documentation in `ARCHITECTURE.md`

---

**Congratulations!** Your professional Library Assistant is now set up and ready for testing and deployment.
