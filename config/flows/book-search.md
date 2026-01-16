# Book Search Flow Configuration

## Overview
The Book Search Flow handles all book discovery and search functionality with advanced filtering, rich results display, and hold placement.

## Flow Structure

### Search Entry Page

**Purpose**: Initial entry point for book searches

**Entry Fulfillment**:
```
I can help you search for books! You can search by:
• Title
• Author
• ISBN
• Genre or subject
• Keywords

What would you like to search for?
```

**Routes**:

1. **Route: Search Intent**
   - **Condition**: `$intent.name == "SearchBooks" OR $intent.name == "FindBook"`
   - **Target Page**: Search Form Page
   - **Transition**: Navigate to form

2. **Route: Browse Intent**
   - **Condition**: `$intent.name == "BrowseBooks" OR $intent.name == "BrowseByGenre"`
   - **Target Page**: Browse Page
   - **Transition**: Navigate to browse

3. **Route: Recommendations Intent**
   - **Condition**: `$intent.name == "GetRecommendations"`
   - **Target Page**: Recommendations Page
   - **Transition**: Navigate to recommendations

---

### Search Form Page

**Purpose**: Collect search parameters through form

**Form Parameters**:

1. **search_type** (Required)
   - **Type**: Custom Entity (@SearchType)
   - **Prompt**: "What would you like to search by? Title, author, ISBN, genre, or keyword?"
   - **Reprompt**: "Please specify: title, author, ISBN, genre, or keyword"

2. **book_title** (Conditional - if search_type is "title")
   - **Type**: Custom Entity (@BookTitle)
   - **Prompt**: "What's the title of the book?"
   - **Reprompt**: "I didn't catch that. What book title are you looking for?"

3. **author** (Conditional - if search_type is "author")
   - **Type**: Custom Entity (@AuthorName)
   - **Prompt**: "Who is the author?"
   - **Reprompt**: "Please tell me the author's name"

4. **isbn** (Conditional - if search_type is "isbn")
   - **Type**: @sys.number-sequence
   - **Prompt**: "What's the ISBN number?"
   - **Reprompt**: "Please provide the ISBN number"

5. **genre** (Conditional - if search_type is "genre")
   - **Type**: Custom Entity (@Genre)
   - **Prompt**: "Which genre are you interested in?"
   - **Reprompt**: "Please specify a genre (e.g., Fiction, Non-fiction, Science, History)"

6. **subject** (Conditional - if search_type is "keyword")
   - **Type**: @sys.any
   - **Prompt**: "What keywords would you like to search for?"
   - **Reprompt**: "Please provide search keywords"

**Routes**:

1. **Route: Form Filled**
   - **Condition**: `$page.params.status == "FINAL"`
   - **Target Page**: Search Results Page
   - **Fulfillment**: Call webhook to perform search
   - **Transition**: Navigate after form completion

2. **Route: Cancel Search**
   - **Condition**: `$intent.name == "Cancel" OR $intent.name == "GoBack"`
   - **Target Flow**: Main Navigation Flow
   - **Transition**: Return to main menu

**Event Handlers**:

1. **sys.no-match-1** (search_type missing)
   - **Fulfillment**: "I need to know what you'd like to search by. You can search by title, author, ISBN, genre, or keyword."
   - **Quick Replies**: ["By title", "By author", "By genre", "By keyword"]

2. **sys.invalid-parameter**
   - **Fulfillment**: "I didn't understand that. Could you please try again?"

---

### Search Results Page

**Purpose**: Display search results with rich formatting

**Entry Fulfillment**:
- **Webhook**: Enabled
- **Webhook Tag**: book-search-webhook

**Routes**:

1. **Route: View Book Details**
   - **Condition**: `$intent.name == "ViewBookDetails" OR $page.params.selected_book != null`
   - **Target Page**: Book Details Page
   - **Transition**: Navigate to details

2. **Route: Place Hold**
   - **Condition**: `$intent.name == "PlaceHold" OR $page.params.hold_action == "place"`
   - **Target Page**: Hold Placement Page
   - **Transition**: Navigate to hold placement

3. **Route: Refine Search**
   - **Condition**: `$intent.name == "RefineSearch" OR $intent.name == "NarrowSearch"`
   - **Target Page**: Search Form Page
   - **Transition**: Return to form

4. **Route: New Search**
   - **Condition**: `$intent.name == "SearchBooks"`
   - **Target Page**: Search Form Page
   - **Transition**: Start new search

5. **Route: Get Recommendations**
   - **Condition**: `$intent.name == "GetRecommendations"`
   - **Target Page**: Recommendations Page
   - **Transition**: Navigate to recommendations

**Rich Response Format**:
- **Single Result**: Card with book details, image, and action buttons
- **Multiple Results**: List with book titles, authors, and images
- **No Results**: Helpful message with suggestions

**Quick Replies** (when results found):
- "Show more results"
- "Refine search"
- "Get recommendations"
- "New search"

---

### Book Details Page

**Purpose**: Display detailed book information

**Entry Fulfillment**:
- **Webhook**: Enabled
- **Webhook Tag**: book-details-webhook

**Routes**:

1. **Route: Place Hold**
   - **Condition**: `$intent.name == "PlaceHold"`
   - **Target Page**: Hold Placement Page
   - **Transition**: Navigate to hold

2. **Route: Check Availability**
   - **Condition**: `$intent.name == "CheckAvailability"`
   - **Target Page**: Stay on page
   - **Fulfillment**: Show availability status

3. **Route: View Similar Books**
   - **Condition**: `$intent.name == "ViewSimilar"`
   - **Target Page**: Search Results Page
   - **Transition**: Show similar books

**Rich Response**:
- **Card Format** with:
  - Book cover image
  - Title, author, ISBN
  - Description
  - Availability status
  - Location information
  - Action buttons (Place Hold, Check Availability, View Similar)

---

### Hold Placement Page

**Purpose**: Place holds on books

**Form Parameters**:

1. **book_id** (Required)
   - **Type**: @sys.number
   - **Prompt**: "Which book would you like to place on hold?"
   - **Reprompt**: "Please specify the book"

2. **pickup_location** (Optional)
   - **Type**: Custom Entity (@LibraryLocation)
   - **Prompt**: "Which location would you like to pick it up from?"
   - **Default**: Main library

**Routes**:

1. **Route: Hold Placed**
   - **Condition**: `$page.params.status == "FINAL"`
   - **Target Page**: Hold Confirmation Page
   - **Fulfillment**: Call webhook to place hold
   - **Transition**: Navigate to confirmation

2. **Route: Cancel Hold**
   - **Condition**: `$intent.name == "Cancel"`
   - **Target Flow**: Main Navigation Flow
   - **Transition**: Return to main menu

**Event Handlers**:

1. **sys.invalid-parameter**
   - **Fulfillment**: "I couldn't process that hold. Please try again or contact support."

---

### Recommendations Page

**Purpose**: Provide personalized book recommendations

**Entry Fulfillment**:
- **Webhook**: Enabled
- **Webhook Tag**: recommendations-webhook

**Routes**:

1. **Route: View Recommendation Details**
   - **Condition**: `$intent.name == "ViewBookDetails"`
   - **Target Page**: Book Details Page
   - **Transition**: Navigate to details

2. **Route: Get More Recommendations**
   - **Condition**: `$intent.name == "GetRecommendations"`
   - **Target Page**: Stay on page
   - **Fulfillment**: Fetch more recommendations

3. **Route: Place Hold on Recommendation**
   - **Condition**: `$intent.name == "PlaceHold"`
   - **Target Page**: Hold Placement Page
   - **Transition**: Navigate to hold

**Rich Response**:
- **List Format** with personalized recommendations
- Each item shows: Title, Author, Why recommended, Cover image

---

### Browse Page

**Purpose**: Browse books by category

**Routes**:

1. **Route: Browse by Genre**
   - **Condition**: `$intent.name == "BrowseByGenre"`
   - **Target Page**: Genre Selection Page
   - **Transition**: Navigate to genre selection

2. **Route: Browse by Subject**
   - **Condition**: `$intent.name == "BrowseBySubject"`
   - **Target Page**: Subject Selection Page
   - **Transition**: Navigate to subject selection

**Rich Response**:
- **Quick Replies** with popular genres/subjects
- **List** of available categories

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
- `search_query`: Current search query
- `search_results`: Search results data
- `selected_book`: Currently selected book
- `search_filters`: Applied search filters

**Webhook Configuration**:
- **Webhook**: library-assistant-webhook
- **Enabled for**: All pages requiring data retrieval

---

## Advanced Features

### 1. Fuzzy Matching
- Enable fuzzy matching for book titles
- Handle typos and variations
- Suggest corrections

### 2. Search Suggestions
- Provide search suggestions as user types
- Auto-complete functionality
- Popular searches

### 3. Filtering
- Filter by availability
- Filter by format (print, ebook, audiobook)
- Filter by language
- Filter by publication date

### 4. Pagination
- Handle large result sets
- "Show more" functionality
- Result count display

### 5. Context Awareness
- Remember previous searches
- Suggest related searches
- Maintain search history

---

## Testing Scenarios

1. **Basic Search**: Search by title, author, ISBN
2. **Advanced Search**: Multi-criteria search
3. **No Results**: Handle empty result sets
4. **Form Validation**: Test parameter collection
5. **Rich Responses**: Verify cards and lists display
6. **Hold Placement**: Test hold workflow
7. **Recommendations**: Test recommendation engine
8. **Error Handling**: Test API failures and edge cases
