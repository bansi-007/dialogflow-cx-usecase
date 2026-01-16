# Main Navigation Flow Configuration

## Overview
The Main Navigation Flow serves as the entry point and central routing hub for the Library Assistant. It handles initial greetings, intent classification, and routes users to specialized flows.

## Flow Structure

### Start Page

**Purpose**: Initial entry point with welcome message and main menu

**Entry Fulfillment**:
```
Welcome to the Library Assistant! I'm here to help you with:
• Searching for books and resources
• Managing your account (checkouts, renewals, holds)
• Making reservations (study rooms, equipment, events)
• Getting help and information

What would you like to do today?
```

**Rich Response - Quick Replies**:
- "Search for books"
- "View my account"
- "Make a reservation"
- "Get help"

**Routes**:

1. **Route: Book Search Intent**
   - **Condition**: `$intent.name == "SearchBooks" OR $intent.name == "FindBook"`
   - **Target Flow**: Book Search Flow
   - **Transition**: Navigate to Book Search Flow

2. **Route: Account Management Intent**
   - **Condition**: `$intent.name == "ViewAccount" OR $intent.name == "ViewCheckouts" OR $intent.name == "ManageAccount"`
   - **Target Flow**: Account Management Flow
   - **Transition**: Navigate to Account Management Flow

3. **Route: Reservations Intent**
   - **Condition**: `$intent.name == "MakeReservation" OR $intent.name == "BookRoom" OR $intent.name == "ReserveEquipment"`
   - **Target Flow**: Reservations Flow
   - **Transition**: Navigate to Reservations Flow

4. **Route: Help Intent**
   - **Condition**: `$intent.name == "GetHelp" OR $intent.name == "AskQuestion" OR $intent.name == "FAQ"`
   - **Target Flow**: Help & FAQ Flow
   - **Transition**: Navigate to Help & FAQ Flow

5. **Route: Greeting Intent**
   - **Condition**: `$intent.name == "Greeting" OR $intent.name == "Hello"`
   - **Target Page**: Stay on Start Page
   - **Fulfillment**: Personalized greeting based on session

6. **Route: Default Fallback**
   - **Condition**: `true`
   - **Target Page**: Stay on Start Page
   - **Fulfillment**: Clarification message with suggestions

**Event Handlers**:

1. **sys.welcome**
   - **Fulfillment**: Welcome message with main menu
   - **Transition**: Stay on page

2. **sys.no-match-default**
   - **Fulfillment**: "I didn't quite understand. Would you like to search for books, manage your account, make a reservation, or get help?"
   - **Quick Replies**: ["Search books", "My account", "Reservations", "Help"]
   - **Transition**: Stay on page

3. **sys.no-input-default**
   - **Fulfillment**: "I'm still here! How can I help you today?"
   - **Transition**: Stay on page

---

### Intent Router Page

**Purpose**: Advanced intent classification and routing

**Routes**:

1. **Route: Book-Related Queries**
   - **Condition**: Contains book-related keywords OR intent confidence > 0.7
   - **Target Flow**: Book Search Flow

2. **Route: Account-Related Queries**
   - **Condition**: Contains account-related keywords
   - **Target Flow**: Account Management Flow

3. **Route: Reservation-Related Queries**
   - **Condition**: Contains reservation-related keywords
   - **Target Flow**: Reservations Flow

4. **Route: Help-Related Queries**
   - **Condition**: Contains help-related keywords
   - **Target Flow**: Help & FAQ Flow

**Conditional Logic**:
- Check user authentication status
- Route to Authentication Flow if not authenticated and account action requested
- Preserve context when transitioning

---

## Flow-Level Settings

**Settings**:
- **Default Language**: English (en)
- **Speech Settings**: Enable speech recognition
- **Advanced Settings**:
  - Enable multi-turn conversation
  - Enable context preservation
  - Enable session variables

**Session Variables**:
- `user_id`: User identifier
- `authenticated`: Authentication status
- `current_flow`: Current flow context
- `search_context`: Search-related context

**Transitions to Other Flows**:
- Book Search Flow
- Account Management Flow
- Reservations Flow
- Help & FAQ Flow
- Authentication Flow (conditional)

---

## Best Practices

1. **Clear Navigation**: Always provide clear options for users
2. **Context Preservation**: Maintain user context across flows
3. **Graceful Fallbacks**: Handle unrecognized inputs gracefully
4. **Quick Actions**: Provide quick reply buttons for common actions
5. **Personalization**: Use session variables for personalized responses

---

## Testing Scenarios

1. **Welcome Message**: Verify welcome message displays correctly
2. **Intent Routing**: Test routing to appropriate flows
3. **Fallback Handling**: Test unrecognized inputs
4. **Context Preservation**: Verify context maintained across transitions
5. **Quick Replies**: Test quick reply functionality
