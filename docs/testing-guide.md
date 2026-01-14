# DialogFlow CX Testing Guide

## Testing Overview

This guide provides comprehensive testing procedures for your DialogFlow CX agent to ensure all features work correctly.

## Pre-Testing Checklist

- [ ] Agent is created and configured
- [ ] All intents are created with training phrases
- [ ] Entities are configured with synonyms
- [ ] Webhook is deployed and accessible
- [ ] Flows and pages are set up
- [ ] Event handlers are configured
- [ ] OpenWeatherMap API key is set (for weather intent)

## Testing Methods

### 1. DialogFlow CX Test Agent

**Location**: DialogFlow CX Console → Test Agent panel (right sidebar)

#### Basic Testing Steps

1. **Open Test Agent**
   - Click "Test Agent" in the right sidebar
   - The test panel will open

2. **Test Intent Recognition**
   ```
   User: "What's the weather in New York?"
   Expected: GetWeather intent recognized, city parameter extracted
   ```

3. **Test Entity Extraction**
   ```
   User: "Weather in NYC"
   Expected: City entity extracted as "New York" (synonym match)
   ```

4. **Test Parameter Extraction**
   ```
   User: "Tell me the weather for London"
   Expected: city parameter = "London"
   ```

5. **Test Webhook Fulfillment**
   ```
   User: "What's the weather in Tokyo?"
   Expected: Webhook called, weather data returned
   ```

---

## Test Cases

### Test Case 1: Weather Intent - Basic Query

**Input**: "What's the weather in Paris?"

**Expected Results**:
- ✅ Intent: GetWeather recognized
- ✅ Entity: City = "Paris" extracted
- ✅ Parameter: city = "Paris"
- ✅ Webhook: Called successfully
- ✅ Response: Contains temperature, description, humidity

**Steps**:
1. Enter the query in Test Agent
2. Check intent recognition
3. Verify parameter extraction
4. Confirm webhook response
5. Validate response message

---

### Test Case 2: Weather Intent - City Synonym

**Input**: "Weather in SF"

**Expected Results**:
- ✅ Intent: GetWeather recognized
- ✅ Entity: City = "San Francisco" (synonym match)
- ✅ Parameter: city = "San Francisco"
- ✅ Webhook: Called with correct city
- ✅ Response: Weather for San Francisco

**Steps**:
1. Enter query with city synonym
2. Verify synonym matching
3. Check parameter value
4. Confirm webhook uses correct city

---

### Test Case 3: Weather Intent - Missing City

**Input**: "What's the weather?"

**Expected Results**:
- ✅ Intent: GetWeather recognized
- ✅ Parameter: city missing
- ✅ Form: Prompts for city name
- ✅ User provides city
- ✅ Webhook: Called with city
- ✅ Response: Weather information

**Steps**:
1. Enter query without city
2. Verify form prompt appears
3. Provide city name
4. Confirm completion

---

### Test Case 4: Greeting Intent - Basic

**Input**: "Hello"

**Expected Results**:
- ✅ Intent: GetGreeting recognized
- ✅ Webhook: Called
- ✅ Response: Generic greeting message

**Steps**:
1. Enter greeting
2. Verify intent recognition
3. Check webhook response
4. Validate greeting message

---

### Test Case 5: Greeting Intent - With Name

**Input**: "Hi, my name is John"

**Expected Results**:
- ✅ Intent: GetGreeting recognized
- ✅ Entity: Name = "John" extracted
- ✅ Parameter: name = "John"
- ✅ Webhook: Called with name
- ✅ Response: Personalized greeting with name

**Steps**:
1. Enter greeting with name
2. Verify name extraction
3. Check personalized response

---

### Test Case 6: Help Intent

**Input**: "What can you do?"

**Expected Results**:
- ✅ Intent: GetHelp recognized
- ✅ Webhook: Called
- ✅ Response: Detailed help information with features

**Steps**:
1. Enter help query
- Verify intent recognition
3. Check webhook response
4. Validate help content

---

### Test Case 7: Flow Navigation

**Input Sequence**:
1. "Hello" → Should navigate to Greeting Page
2. "What's the weather in London?" → Should navigate to Weather Handling Page
3. "Help" → Should navigate to Help Page

**Expected Results**:
- ✅ Each intent navigates to correct page
- ✅ Conversation context maintained
- ✅ Transitions are smooth

**Steps**:
1. Start conversation
2. Test each navigation
3. Verify page transitions
4. Check context preservation

---

### Test Case 8: Event Handler - No Match

**Input**: "asdfghjkl" (gibberish)

**Expected Results**:
- ✅ Intent: Default Negative Intent
- ✅ Event: sys.no-match-default triggered
- ✅ Response: Helpful error message
- ✅ User can retry

**Steps**:
1. Enter unrecognized input
2. Verify event handler triggers
3. Check error message
4. Test recovery path

---

### Test Case 9: Event Handler - No Input

**Scenario**: User doesn't respond to prompt

**Expected Results**:
- ✅ Event: sys.no-input-default triggered
- ✅ Response: Encouraging message
- ✅ Conversation continues

**Steps**:
1. Trigger a prompt (e.g., ask for city)
2. Wait or send empty input
3. Verify event handler
4. Check response

---

### Test Case 10: Webhook Error Handling

**Input**: "What's the weather in InvalidCity123?"

**Expected Results**:
- ✅ Intent: GetWeather recognized
- ✅ Webhook: Called
- ✅ API: Returns error (city not found)
- ✅ Response: User-friendly error message
- ✅ User can retry

**Steps**:
1. Enter query with invalid city
2. Verify webhook error handling
3. Check error response
4. Test retry capability

---

## Advanced Testing

### 1. Multi-Turn Conversation

Test a complete conversation flow:

```
User: "Hello"
Agent: "Hello! How can I help you today?"

User: "What's the weather in New York?"
Agent: [Weather information for New York]

User: "What about London?"
Agent: [Weather information for London]

User: "Thanks!"
Agent: "You're welcome! Have a great day!"
```

**Verify**:
- Context is maintained
- Follow-up questions work
- City parameter updates correctly

---

### 2. Parameter Validation

Test form parameter collection:

```
User: "What's the weather?"
Agent: "Which city would you like to know the weather for?"
User: "Tokyo"
Agent: [Weather information]
```

**Verify**:
- Form prompts correctly
- Parameter is collected
- Validation works

---

### 3. Webhook Integration Testing

Test webhook directly:

```bash
curl -X POST https://YOUR-WEBHOOK-URL \
  -H "Content-Type: application/json" \
  -d '{
    "sessionInfo": {
      "session": "test-session",
      "parameters": {
        "city": "London"
      }
    },
    "intentInfo": {
      "displayName": "GetWeather"
    }
  }'
```

**Verify**:
- Webhook responds correctly
- API integration works
- Error handling functions

---

## Testing Checklist

### Intent Testing
- [ ] All intents recognize correctly
- [ ] Training phrases work
- [ ] Similar phrases don't trigger wrong intents
- [ ] Fallback intent works

### Entity Testing
- [ ] Entities extract correctly
- [ ] Synonyms match properly
- [ ] Fuzzy matching works
- [ ] System entities function

### Parameter Testing
- [ ] Parameters extract from utterances
- [ ] Required parameters prompt correctly
- [ ] Parameter validation works
- [ ] Parameters pass to webhook

### Webhook Testing
- [ ] Webhook receives requests
- [ ] Webhook processes correctly
- [ ] External API integration works
- [ ] Error handling functions
- [ ] Response format is correct

### Flow Testing
- [ ] Page transitions work
- [ ] Forms collect parameters
- [ ] Routes function correctly
- [ ] Context is maintained

### Event Handler Testing
- [ ] No-match events handled
- [ ] No-input events handled
- [ ] Cancel events handled
- [ ] Custom events work

### User Experience Testing
- [ ] Responses are natural
- [ ] Error messages are helpful
- [ ] Conversation flows smoothly
- [ ] Recovery paths work

---

## Debugging Tips

1. **Check Logs**
   - View Cloud Functions logs for webhook issues
   - Check DialogFlow CX logs for intent/entity problems

2. **Test Incrementally**
   - Test one feature at a time
   - Verify each component before moving on

3. **Use Test Agent**
   - Utilize the built-in test agent for quick testing
   - Check intent confidence scores

4. **Verify Webhook URL**
   - Ensure webhook URL is correct
   - Check webhook is accessible
   - Verify authentication if required

5. **Check API Keys**
   - Verify OpenWeatherMap API key is set
   - Test API key independently

---

## Performance Testing

1. **Response Time**
   - Measure webhook response time
   - Target: < 2 seconds for weather queries

2. **Concurrent Requests**
   - Test multiple simultaneous requests
   - Verify no conflicts or errors

3. **Error Rate**
   - Monitor error rates
   - Identify common failure points

---

## Continuous Improvement

After testing, iterate based on findings:

1. **Add Training Phrases**: Based on failed recognitions
2. **Improve Entity Synonyms**: Add missing variations
3. **Enhance Error Messages**: Make them more helpful
4. **Optimize Flows**: Simplify complex navigation
5. **Update Webhook Logic**: Handle edge cases better
