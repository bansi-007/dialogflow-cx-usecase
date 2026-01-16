# Manual Testing Guide: Book Search Flow

## 1. Local Testing (Recommended First Step)
Before testing in the Dialogflow CX Console, verify your logic works locally using the script we created.
1. Open a terminal.
2. Run: `python3 cloud-functions/test_search_flow.py`
3. Enter a book title (e.g., "The Great Gatsby").
4. **Success Criteria**: You see a JSON response with book details and "I found a book matching your search".

## 2. Dialogflow CX Console Configuration
To enable the Search Flow in the console, ensure the following configuration matches your deployed code.

### A. Intents
1. **SearchBooks** Intent:
   - Ensure you have training phrases like "Search for books", "Find a book".
   - **Parameters**: make sure `book_title` is defined as an entity (e.g., `@sys.any` or `@BookTitle`) if you want to extract it directly.

### B. Flow & Page Setup
1. Go to **Build** tab.
2. Create a Flow named **"Book Search Flow"** (Case sensitive! Your webhook relies on this name).
3. In the **Start Page** of this flow:
   - Add a **Route**.
   - **Intent**: `SearchBooks`
   - **Condition**: `true` (or leave empty)
   - **Fulfillment**: 
     - Check **Enable Webhook**.
     - Tag: `book-search-webhook` (Optional, but good practice).
   - **Transition**: You can transition to a "Display Results" page or stay on the Start Page.

### C. Webhook Settings
1. Go to **Manage** > **Webhooks**.
2. Create/Edit the webhook.
   - **URL**: [Paste your Cloud Function URL here]
   - **Timeouts**: Increase to 10s or 15s.

## 3. Simulator Testing
1. Click **Test Agent** (Simulator) in top right.
2. Select **Environment**: Draft.
3. Select **Flow**: Book Search Flow (or Default Start Flow if you are routing from there).
4. **Input**: "Search for The Great Gatsby"
5. **Debug Analysis**:
   - look at the **Diagnostic Info** (bottom right of simulator response).
   - Check **Execution Steps** -> **Webhook Request**.
   - **Verify**:
      - `fulfillmentInfo.tag` matches what you set (if any).
      - `intentInfo.parameters` contains `book_title: "The Great Gatsby"`.
      - `pageInfo.currentFlow.displayName` is "Book Search Flow" (CRITICAL for your router).

## 4. Troubleshooting
- **Error: "Webhook call failed"**: Check Cloud Function logs. `gcloud functions logs read library-assistant-webhook ...`
- **Generic Response / No Search Results**: 
   - Check if the **Flow Name** in the simulator matches "Book Search Flow". Even if you are in the default flow, ensure the webhook logic (`main.py` lines 120+) can handle it. *Note: Your current code explicitly checks `if flow_name == "Book Search Flow"` OR `"book" in intent_name`. so sticking to "Book Search Flow" is safest.*
