# Next Steps - After Importing Entities

## ✅ What You've Completed

- [x] Created DialogFlow CX Agent
- [x] Deployed Cloud Functions Webhook
- [x] Configured Webhook in DialogFlow CX
- [x] Created and Imported Entities (BookTitle, AuthorName, Genre, etc.)

## 🎯 Next Steps (In Order)

### Step 1: Create Intents (Priority: High)

Create the main intents that users will interact with.

**Location**: `config/intents/`

**Files to follow**:
- `book-search-intents.md` - Book search intents
- `account-intents.md` - Account management intents

**Quick Start - Book Search Intents**:

1. Go to **Intents** (under Resources)
2. Create these intents:
   - **SearchBooks** - Main book search intent
   - **FindBook** - Alternative search intent
   - **PlaceHold** - Place holds on books
   - **GetRecommendations** - Book recommendations

3. For each intent:
   - Add training phrases (10-20 variations)
   - Configure parameters (use the entities you just imported)
   - Enable webhook fulfillment
   - Add default responses

**Example - SearchBooks Intent**:
- **Training Phrases**: "Search for books", "Find a book", "I'm looking for a book", etc.
- **Parameters**: 
  - `book_title` (Entity: @BookTitle)
  - `author` (Entity: @AuthorName)
  - `genre` (Entity: @Genre)
- **Webhook**: Enable for fulfillment

---

### Step 2: Create Flows and Pages (Priority: High)

Set up the conversation structure with flows and pages.

**Location**: `config/flows/`

**Start with Main Navigation Flow**:

1. Go to **Flows**
2. Use the default flow or create **"Main Navigation Flow"**
3. Follow `config/flows/main-navigation.md`:
   - Create **Start Page** with welcome message
   - Add routes to other flows
   - Configure event handlers

**Then Create Book Search Flow**:

1. Create new flow: **"Book Search Flow"**
2. Follow `config/flows/book-search.md`:
   - Create **Search Entry Page**
   - Create **Search Form Page** (collect parameters)
   - Create **Search Results Page** (display results)
   - Configure routes and transitions
   - Enable webhook for data retrieval

---

### Step 3: Test Basic Flow (Priority: Medium)

Test that everything works together.

1. Go to **Test Agent** panel
2. Try: "Search for books"
3. Verify:
   - Intent is recognized
   - Entities are extracted
   - Webhook is called
   - Response is returned

---

### Step 4: Create Account Management Flow (Priority: High)

Set up account-related functionality.

1. Create **"Account Management Flow"**
2. Follow `config/flows/account-management.md`:
   - Create pages for checkouts, renewals, holds, fines
   - Configure authentication checks
   - Set up account operations

---

### Step 5: Configure Rich Responses (Priority: Medium)

Make responses more visual and interactive.

**Location**: `config/advanced-features/rich-responses.md`

1. Add **Card responses** for book information
2. Add **List responses** for search results
3. Add **Quick reply buttons** for common actions

**Example - Book Card**:
- Title, author, cover image
- Action buttons: "Place Hold", "View Details"

---

### Step 6: Set Up Event Handlers (Priority: Medium)

Handle errors and edge cases gracefully.

1. Add flow-level event handlers:
   - `sys.no-match-default` - Unrecognized input
   - `sys.no-input-default` - No user input
   - `sys.cancel` - User cancels

2. Add page-level event handlers:
   - Parameter validation errors
   - Form completion errors

---

### Step 7: Create More Intents (Priority: Medium)

Add remaining intents for complete functionality.

**Account Intents**:
- ViewCheckouts
- RenewBook
- ViewHolds
- PayFines

**Reservation Intents**:
- BookRoom
- ReserveEquipment
- RegisterForEvent

---

### Step 8: Configure Knowledge Connector (Optional)

Set up FAQ handling.

1. Go to **Knowledge** (under Resources)
2. Create **Knowledge Base**
3. Add FAQ documents or entries
4. Connect to **Help & FAQ Flow**

---

## 📋 Recommended Order

**Week 1 - Core Functionality**:
1. ✅ Entities (Done!)
2. ⏭️ Create Book Search Intents
3. ⏭️ Create Main Navigation Flow
4. ⏭️ Create Book Search Flow
5. ⏭️ Test basic book search

**Week 2 - Account Features**:
6. ⏭️ Create Account Management Flow
7. ⏭️ Create Account Intents
8. ⏭️ Test account features

**Week 3 - Polish**:
9. ⏭️ Add Rich Responses
10. ⏭️ Configure Event Handlers
11. ⏭️ Add more intents
12. ⏭️ Comprehensive testing

---

## 🚀 Quick Start - Do This Now

**Immediate Next Step**: Create the **SearchBooks** intent

1. Go to **Intents** → **Create Intent**
2. Name: **SearchBooks**
3. Add training phrases:
   - "Search for books"
   - "Find a book"
   - "I'm looking for a book"
   - "Do you have [book title]?"
   - "Search the catalog"
   - (Add 10-15 more variations)

4. Add parameters:
   - `book_title` (Entity: @BookTitle)
   - `author` (Entity: @AuthorName)
   - `genre` (Entity: @Genre)

5. Enable webhook fulfillment

6. Add default response: "I'll help you search for books."

7. **Test it!** Use Test Agent panel

---

## 📚 Reference Files

- **Intents**: `config/intents/book-search-intents.md`
- **Flows**: `config/flows/main-navigation.md`, `config/flows/book-search.md`
- **Setup Guide**: `docs/setup-guide.md` (Step 6 onwards)

---

## 💡 Tips

1. **Start Small**: Get one flow working end-to-end before adding more
2. **Test Frequently**: Test after each major change
3. **Use Test Agent**: The Test Agent panel is your best friend
4. **Check Logs**: If webhook fails, check Cloud Functions logs
5. **Iterate**: Don't try to build everything at once

---

- [x] Create Book Search Intents (SearchBooks imported)
- [x] Manual Verification (See MANUAL_TESTING_GUIDE.md)
- [x] Test Basic Search Flow (Done in Simulator)

- [x] Create Account Management Flow & Route (Verified)
- [x] Create Reservations & Help Flows (Verified)
- [x] Fix Webhook Routing Bug (BookRoom vs Search)

**Current Status:** The High-Level Agent Architecture is **COMPLETE**. All 4 major flows are created, wired up, and routing correctly for logged-in/logged-out states.

**Next Immediate Step:** 
- [x] Create Test Cases: **DONE (4/4 Passing)**. Architecture is verified and locked in.

**Conclusion of Session:**
The High-Level Agent Architecture is fully built and verified. We have a robust "Router" that correctly handles all major user intents and dispatches them to specialized flows, backed by a functional Cloud Function webhook with correct Logic.

**Next Session Goal:**
- [x] **Implement Authentication Flow**: **DONE**. Users can now successfully log in, and the agent automatically redirects them back to their dashboard with rich account details.

**Next Immediate Step:**
- [ ] **Account Flow Detail**: Now that we can log in, we need to implement the actual features: "View Checkouts", "Renew Books", and "Pay Fines". We will start by creating the pages and routes for these actions within the Account Management Flow.

**Future Implementation:**
- [ ] **Reservations Detail**: Add form filling for Date/Time/Room.
- [ ] **Help & FAQ Detail**: Add static responses or knowledge base integration.

