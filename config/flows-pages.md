# Flows and Pages Configuration

This document outlines the conversation flow structure using flows and pages in DialogFlow CX.

## Default Flow Structure

### Flow: Default Start Flow

**Purpose**: Main conversation flow that handles all user interactions.

---

## Page 1: Welcome Page

**Purpose**: Initial page that greets users and sets context.

### Entry Fulfillment
- **Agent Response**: "Welcome! I'm your weather assistant. How can I help you today?"

### Routes
1. **Route: Weather Query**
   - **Intent**: GetWeather
   - **Condition**: `$intent.name == "GetWeather"`
   - **Target Page**: Weather Handling Page
   - **Transition**: Navigate to Weather Handling Page

2. **Route: Greeting**
   - **Intent**: GetGreeting
   - **Condition**: `$intent.name == "GetGreeting"`
   - **Target Page**: Greeting Page
   - **Transition**: Navigate to Greeting Page

3. **Route: Help Request**
   - **Intent**: GetHelp
   - **Condition**: `$intent.name == "GetHelp"`
   - **Target Page**: Help Page
   - **Transition**: Navigate to Help Page

4. **Route: Default Fallback**
   - **Intent**: Default Negative Intent
   - **Condition**: `true`
   - **Target Page**: Stay on Welcome Page
   - **Transition**: Show clarification message

### Form (Optional)
- No form on welcome page

---

## Page 2: Weather Handling Page

**Purpose**: Handle weather-related queries and extract city parameter.

### Entry Fulfillment
- **Agent Response**: "I'll help you with weather information."

### Form
- **Parameter**: `city`
  - **Required**: Yes
  - **Prompt**: "Which city would you like to know the weather for?"
  - **Reprompt**: "I didn't catch that. Could you please tell me the city name again?"

### Routes
1. **Route: Weather Fulfilled**
   - **Condition**: `$page.params.status == "FINAL"`
   - **Target Page**: Weather Response Page
   - **Transition**: Navigate after form completion

2. **Route: Cancel**
   - **Intent**: Default Negative Intent
   - **Condition**: User wants to cancel
   - **Target Page**: Welcome Page
   - **Transition**: Return to welcome

### Fulfillment
- **Webhook**: Enabled
- **Webhook Tag**: weather-webhook

---

## Page 3: Weather Response Page

**Purpose**: Display weather information retrieved from webhook.

### Entry Fulfillment
- **Agent Response**: Uses webhook response (dynamic)
- **Webhook**: Enabled

### Routes
1. **Route: Another Query**
   - **Intent**: GetWeather
   - **Condition**: `$intent.name == "GetWeather"`
   - **Target Page**: Weather Handling Page
   - **Transition**: Handle new weather query

2. **Route: Return to Welcome**
   - **Intent**: GetGreeting or GetHelp
   - **Condition**: `$intent.name == "GetGreeting" OR $intent.name == "GetHelp"`
   - **Target Page**: Welcome Page
   - **Transition**: Return to main flow

3. **Route: End Session**
   - **Intent**: Default Negative Intent (with "goodbye", "thanks", etc.)
   - **Condition**: User indicates end of conversation
   - **Target Page**: End Flow
   - **Transition**: End conversation

---

## Page 4: Greeting Page

**Purpose**: Handle user greetings and introductions.

### Entry Fulfillment
- **Agent Response**: Uses webhook response (personalized greeting)
- **Webhook**: Enabled

### Routes
1. **Route: Weather Query**
   - **Intent**: GetWeather
   - **Condition**: `$intent.name == "GetWeather"`
   - **Target Page**: Weather Handling Page
   - **Transition**: Navigate to weather flow

2. **Route: Help Request**
   - **Intent**: GetHelp
   - **Condition**: `$intent.name == "GetHelp"`
   - **Target Page**: Help Page
   - **Transition**: Navigate to help

3. **Route: Continue Conversation**
   - **Condition**: `true`
   - **Target Page**: Welcome Page
   - **Transition**: Return to welcome after greeting

---

## Page 5: Help Page

**Purpose**: Provide users with information about available features.

### Entry Fulfillment
- **Agent Response**: Uses webhook response (detailed help information)
- **Webhook**: Enabled

### Routes
1. **Route: Weather Query**
   - **Intent**: GetWeather
   - **Condition**: `$intent.name == "GetWeather"`
   - **Target Page**: Weather Handling Page
   - **Transition**: Navigate to weather flow

2. **Route: Greeting**
   - **Intent**: GetGreeting
   - **Condition**: `$intent.name == "GetGreeting"`
   - **Target Page**: Greeting Page
   - **Transition**: Navigate to greeting

3. **Route: Return to Welcome**
   - **Condition**: `true`
   - **Target Page**: Welcome Page
   - **Transition**: Return to main flow

---

## Flow Configuration Best Practices

1. **Logical Flow**: Ensure pages follow a logical conversation progression
2. **Clear Transitions**: Use descriptive route names and conditions
3. **Error Handling**: Include fallback routes for unexpected inputs
4. **Parameter Validation**: Use forms to ensure required parameters are collected
5. **Context Preservation**: Maintain conversation context across page transitions
6. **User Experience**: Minimize unnecessary page transitions

## Alternative Flow Structure

### Flow: Weather Flow (Separate Flow)

If you want to create a separate flow for weather queries:

1. **Create New Flow**: "Weather Flow"
2. **Start Page**: Weather Handling Page
3. **Subsequent Pages**: Weather Response Page
4. **Flow Transitions**: 
   - From Default Flow → Weather Flow (when GetWeather intent detected)
   - From Weather Flow → Default Flow (when user wants to return)

This separation can make complex conversations easier to manage.
