# Event Handlers Configuration

This document outlines event handlers to be configured in DialogFlow CX.

## Flow-Level Event Handlers

### Flow: Default Start Flow

#### Event Handler 1: Session Start

**Event**: `sys.no-match-default`
**Trigger**: When no intent matches (fallback scenario)

**Fulfillment**:
- **Agent Response**: "I didn't quite understand that. Could you please rephrase? I can help you with weather information, greetings, or answer questions."

**Transition**:
- **Target**: Stay on current page
- **Condition**: None

---

#### Event Handler 2: No Input

**Event**: `sys.no-input-default`
**Trigger**: When user doesn't provide input after a prompt

**Fulfillment**:
- **Agent Response**: "I'm still here! Please let me know how I can help you. You can ask about weather, say hello, or ask for help."

**Transition**:
- **Target**: Stay on current page
- **Condition**: None

---

#### Event Handler 3: Session End

**Event**: `sys.cancel`
**Trigger**: When user explicitly cancels or ends the session

**Fulfillment**:
- **Agent Response**: "Thank you for using our service! Have a great day!"

**Transition**:
- **Target**: End Flow
- **Condition**: None

---

## Page-Level Event Handlers

### Page: Weather Handling Page

#### Event Handler 1: Form Parameter Missing

**Event**: `sys.no-match-1` (or custom event)
**Trigger**: When required form parameter (city) is not provided

**Fulfillment**:
- **Agent Response**: "I need to know which city you're interested in. Please tell me the city name."

**Transition**:
- **Target**: Stay on current page
- **Condition**: `$page.params.status != "FINAL"`

---

#### Event Handler 2: Invalid City Name

**Event**: Custom event (triggered by webhook validation)
**Trigger**: When webhook determines city name is invalid

**Fulfillment**:
- **Agent Response**: "I couldn't find weather information for that city. Please check the spelling and try again, or provide a different city name."

**Transition**:
- **Target**: Weather Handling Page (to retry)
- **Condition**: None

---

### Page: Welcome Page

#### Event Handler 1: Welcome Message

**Event**: `sys.welcome`
**Trigger**: When user first starts a conversation

**Fulfillment**:
- **Agent Response**: "Hello! Welcome to the Weather Assistant. I can help you with weather information, answer questions, or just have a friendly chat. What would you like to do?"

**Transition**:
- **Target**: Stay on Welcome Page
- **Condition**: None

---

## System Events Reference

DialogFlow CX provides several system events:

1. **sys.no-match-default**: No intent matched
2. **sys.no-input-default**: No user input received
3. **sys.cancel**: User canceled the conversation
4. **sys.welcome**: Session started (welcome event)
5. **sys.invalid-parameter**: Invalid parameter value provided
6. **sys.no-match-N**: No match for specific route (N = route number)

## Custom Events

You can also create custom events in your webhook and trigger them:

### Example: Weather API Error

**Event Name**: `weather-api-error`
**Trigger**: From webhook when API call fails

**Handler Configuration**:
- **Event**: `weather-api-error`
- **Fulfillment**: "I'm having trouble accessing weather data right now. Please try again in a moment."
- **Transition**: Return to Weather Handling Page

---

## Event Handler Best Practices

1. **Comprehensive Coverage**: Handle all common error scenarios
2. **User-Friendly Messages**: Provide clear, helpful error messages
3. **Graceful Degradation**: Always provide a path forward for users
4. **Context Preservation**: Maintain conversation context when handling events
5. **Logging**: Log events for debugging and improvement
6. **Testing**: Test all event handlers thoroughly

## Implementation Steps

1. **Navigate to Flow Settings**
   - Go to your flow in DialogFlow CX console
   - Click on the flow name to access settings

2. **Add Flow-Level Event Handlers**
   - Click "Add Event Handler"
   - Select event type
   - Configure fulfillment and transitions

3. **Add Page-Level Event Handlers**
   - Navigate to specific page
   - Click "Add Event Handler"
   - Configure for that page's context

4. **Test Event Handlers**
   - Use Test Agent to simulate various scenarios
   - Verify handlers trigger correctly
   - Check that responses are appropriate
