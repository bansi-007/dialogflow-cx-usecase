# Library Assistant - Dialogflow CX

A conversational AI agent for library management built with Dialogflow CX and Google Cloud Functions.

## Quick Start

```bash
# 1. Navigate to project
cd /Users/maddali/DialogFlow

# 2. Start server
python3 -m http.server 8080

# 3. Open demo
open http://localhost:8080/demo.html
```

**Demo Credentials:** `user123` / `secretpass`

## Project Structure

```
DialogFlow/
├── demo.html              # Demo page with documentation
├── cloud-functions/       # Python webhook
│   ├── main.py           # Request router
│   ├── utils.py          # Response builder
│   └── library_service.py # Mock API
└── config/intents/csv/   # Intent training data
```

## Architecture

- **Frontend**: Dialogflow Messenger Widget
- **AI**: Dialogflow CX (5 Flows, 15+ Intents)
- **Backend**: Google Cloud Functions (Python 3.11)
- **Database**: Mock data (10+ books)

## Key Features

1. **Book Search** - Search by title, author, genre
2. **Authentication** - Secure login with session management
3. **Account Management** - View checkouts, renew books, check fines
4. **Smart Resume** - Remembers intent across login flows

## Demo Flows

### Flow 1: Search
```
"Search for Harry Potter" → Shows 2 books
```

### Flow 2: Smart Resume
```
"Place hold on Harry Potter" → Login prompt → Auto-completes hold
```

### Flow 3: Account
```
"Login" → "View checkouts" → "Renew The Great Gatsby"
```

## Deployment

```bash
cd cloud-functions
./deploy.sh
```

---

**Demo URL**: http://localhost:8080/demo.html
