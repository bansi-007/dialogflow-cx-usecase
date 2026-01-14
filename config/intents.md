# Intent Definitions

This document outlines the intents to be created in DialogFlow CX.

## Intent 1: GetWeather

**Purpose**: Handle user queries about weather information for a specific city.

### Training Phrases
- "What's the weather in New York?"
- "Tell me the weather for London"
- "How's the weather in Tokyo?"
- "Weather in Paris"
- "What's the temperature in San Francisco?"
- "Is it raining in Seattle?"
- "Weather forecast for Miami"
- "How hot is it in Dubai?"
- "What's the weather like in Boston?"
- "Check weather for Chicago"

### Parameters
- **city** (entity: @sys.geo-city or custom entity)
  - Required: Yes
  - Prompt: "Which city would you like to know the weather for?"

### Response (Default)
"Let me check the weather for {city}."

### Fulfillment
- Enable webhook for this intent
- Webhook will call OpenWeatherMap API and return detailed weather information

---

## Intent 2: GetGreeting

**Purpose**: Handle user greetings and initial interactions.

### Training Phrases
- "Hello"
- "Hi there"
- "Hey"
- "Good morning"
- "Good afternoon"
- "Good evening"
- "Greetings"
- "Hi, my name is John"
- "Hello, I'm Sarah"
- "Hey, call me Mike"

### Parameters
- **name** (entity: @sys.person or custom entity)
  - Required: No
  - Prompt: "What's your name?"

### Response (Default)
"Hello! How can I help you today? I can provide weather information, answer questions, or help with various tasks."

### Fulfillment
- Enable webhook for personalized greeting
- Webhook will use the name parameter if provided

---

## Intent 3: GetHelp

**Purpose**: Provide users with information about available features and capabilities.

### Training Phrases
- "Help"
- "What can you do?"
- "What are your capabilities?"
- "How can you help me?"
- "What features do you have?"
- "Show me what you can do"
- "I need help"
- "Can you help me?"
- "What do you offer?"
- "Tell me about your features"

### Parameters
None required

### Response (Default)
"I'm here to help! I can provide weather information, answer questions, and assist with various tasks. What would you like to know?"

### Fulfillment
- Enable webhook for detailed help information
- Webhook will return comprehensive feature list

---

## Intent Configuration Notes

1. **Intent Priority**: Set appropriate priority levels if there are overlapping phrases
2. **Contexts**: Consider adding input/output contexts for better conversation flow
3. **Training Phrase Coverage**: Ensure training phrases cover various phrasings and user styles
4. **Parameter Prompts**: Make prompts natural and conversational
5. **Fallback Intent**: Ensure default fallback intent is configured for unrecognized queries
