# Agent Dialogs Configuration

This document outlines agent dialogs to be configured in DialogFlow CX.

## What are Agent Dialogs?

Agent dialogs are pre-configured responses that provide context, guidance, and information to users throughout the conversation. They help create a more natural and helpful conversational experience.

## Dialog Types

### 1. Welcome Dialog

**Location**: Flow-level or Start Page

**Purpose**: Greet users when they first interact with the agent.

**Configuration**:
- **Trigger**: Session start or welcome event
- **Message**: "Welcome to the Weather Assistant! I'm here to help you with weather information, answer questions, and assist with various tasks. How can I help you today?"

**Implementation Steps**:
1. Navigate to your Flow (Default Start Flow)
2. Click on the Start Page
3. Add Entry Fulfillment
4. Configure the welcome message

---

### 2. Contextual Help Dialog

**Location**: Page-level (Welcome Page, Help Page)

**Purpose**: Provide contextual help based on the current conversation state.

**Configuration Examples**:

#### Welcome Page Context Dialog
- **Message**: "You can ask me about weather in any city, say hello, or ask for help. Just tell me what you need!"

#### Weather Page Context Dialog
- **Message**: "I can help you get weather information for any city. Just tell me the city name, and I'll provide current weather conditions."

#### Help Page Context Dialog
- **Message**: "I'm here to assist you! I can provide weather information, answer questions, and help with various tasks. What would you like to know more about?"

---

### 3. Clarification Dialog

**Location**: Page-level (when parameters are missing)

**Purpose**: Guide users when required information is missing.

**Configuration**:

#### Weather Page - Missing City
- **Trigger**: When city parameter is not provided
- **Message**: "I'd be happy to help you with weather information! Which city would you like to know about? You can say something like 'New York' or 'London'."

**Implementation**:
- Use Form parameter prompts
- Configure reprompt messages

---

### 4. Confirmation Dialog

**Location**: Page-level (before executing actions)

**Purpose**: Confirm user intent before proceeding with actions.

**Configuration Example**:

#### Weather Confirmation
- **Message**: "I'll check the weather for {city}. Is that correct?"
- **Options**: Yes/No
- **On Yes**: Proceed to webhook
- **On No**: Return to parameter collection

**Note**: This is optional and can be skipped for simple queries.

---

### 5. Error Recovery Dialog

**Location**: Page-level or Flow-level

**Purpose**: Help users recover from errors gracefully.

**Configuration Examples**:

#### Invalid City Error
- **Trigger**: When weather API returns error
- **Message**: "I couldn't find weather information for that city. Please check the spelling and try again, or provide a different city name. You can say something like 'New York', 'London', or 'Tokyo'."

#### Webhook Error
- **Trigger**: When webhook fails
- **Message**: "I'm having trouble accessing that information right now. Please try again in a moment, or ask about something else."

---

### 6. Transition Dialog

**Location**: Between pages

**Purpose**: Smoothly guide users through conversation flow.

**Configuration Examples**:

#### From Greeting to Weather
- **Message**: "Great! Let me help you with weather information. Which city are you interested in?"

#### From Weather to Help
- **Message**: "I can also help you with other things. Would you like to know what else I can do?"

---

### 7. Completion Dialog

**Location**: After successful actions

**Purpose**: Confirm completion and offer next steps.

**Configuration Example**:

#### After Weather Query
- **Message**: "Is there anything else you'd like to know? I can check weather for another city, or help you with other questions."

---

## Implementation Guide

### Step 1: Flow-Level Dialogs

1. **Navigate to Flow Settings**
   - Go to DialogFlow CX Console
   - Select your Flow (Default Start Flow)
   - Click on Flow settings

2. **Configure Entry Fulfillment**
   - Add welcome message
   - Set as entry fulfillment for the flow

3. **Add Event Handlers**
   - Configure dialogs for events (see event-handlers.md)

### Step 2: Page-Level Dialogs

1. **Navigate to Specific Page**
   - Select the page you want to configure

2. **Add Entry Fulfillment**
   - Click "Entry Fulfillment"
   - Add dialog message
   - Configure when it should trigger

3. **Add Form Prompts**
   - For pages with forms
   - Configure parameter prompts
   - Add reprompt messages

### Step 3: Route-Level Dialogs

1. **Navigate to Route**
   - Select a route on a page

2. **Add Fulfillment**
   - Configure dialog for that specific route
   - Use for conditional messages

---

## Dialog Best Practices

### 1. Keep Messages Natural
- Use conversational language
- Avoid technical jargon
- Make it feel like talking to a person

### 2. Be Specific and Helpful
- Provide clear guidance
- Give examples when helpful
- Offer next steps

### 3. Maintain Context
- Reference previous conversation
- Use collected parameters
- Personalize when possible

### 4. Handle Errors Gracefully
- Don't blame the user
- Provide clear recovery paths
- Offer alternatives

### 5. Guide User Actions
- Tell users what they can do
- Provide examples
- Make next steps clear

### 6. Use Variable References
- Reference parameters: `{city}`, `{name}`
- Use session parameters
- Personalize responses

---

## Example Dialog Configurations

### Complete Welcome Flow Dialog

```
Entry Fulfillment (Start Page):
"Welcome! I'm your Weather Assistant. I can help you with:
• Weather information for any city
• Answering questions
• General assistance

What would you like to do?"

Route Dialog (Weather Intent):
"Great! I'll help you get weather information. Which city are you interested in?"

Form Prompt (City Parameter):
Initial: "Which city would you like to know the weather for?"
Reprompt: "I didn't catch that. Could you please tell me the city name? For example, you could say 'New York' or 'London'."

Completion Dialog (After Weather):
"Here's the weather information for {city}. Is there anything else you'd like to know?"
```

---

## Advanced Dialog Features

### 1. Conditional Dialogs
Use conditions to show different dialogs based on context:

```
Condition: $session.params.user_type == "new"
Message: "Welcome! This is your first time here. Let me show you around..."

Condition: $session.params.user_type == "returning"
Message: "Welcome back! How can I help you today?"
```

### 2. Rich Responses
Use rich response types:
- Text messages
- Quick replies
- Cards
- Lists
- Images

### 3. Multi-Turn Dialogs
Design dialogs that span multiple turns:
- Ask follow-up questions
- Collect multiple parameters
- Guide through complex flows

---

## Testing Dialogs

1. **Test Each Dialog**
   - Verify messages appear correctly
   - Check variable substitution
   - Ensure timing is appropriate

2. **Test Dialog Flow**
   - Verify smooth transitions
   - Check context preservation
   - Ensure no dead ends

3. **User Experience**
   - Get feedback on clarity
   - Check if guidance is helpful
   - Verify error recovery works

---

## Dialog Maintenance

1. **Regular Updates**
   - Update based on user feedback
   - Add new dialogs as features expand
   - Refine messages for clarity

2. **A/B Testing**
   - Test different dialog variations
   - Measure effectiveness
   - Optimize based on results

3. **Analytics**
   - Track dialog usage
   - Identify common paths
   - Find improvement opportunities
