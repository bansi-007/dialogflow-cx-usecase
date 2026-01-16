# Professional Library Assistant - DialogFlow CX

A comprehensive, production-ready library assistant chatbot built with DialogFlow CX, featuring advanced conversational AI capabilities, multiple flows, rich responses, and seamless library system integration.

## 🎯 Project Overview

This is a professional-grade library assistant that demonstrates advanced DialogFlow CX features including:
- **Multiple specialized flows** for different use cases
- **Rich responses** (cards, lists, quick replies, images)
- **Knowledge connectors** for FAQ handling
- **Advanced entity extraction** with validation
- **Multi-turn conversations** with state management
- **Conditional routing** and context management
- **Professional UX** with error recovery and fallbacks
- **Library system integration** via webhooks

## 🏗️ Architecture

### Flows Structure

1. **Main Navigation Flow** - Entry point and routing hub
2. **Book Search Flow** - Advanced book search with filters and recommendations
3. **Account Management Flow** - Checkouts, holds, renewals, fines, account info
4. **Reservations Flow** - Study rooms, equipment, event bookings
5. **Help & FAQ Flow** - Knowledge base integration and support
6. **Authentication Flow** - User login and verification

### Key Features

- ✅ **Advanced Search**: Title, author, ISBN, genre, subject, keyword search
- ✅ **Account Management**: View checkouts, renew books, place holds, pay fines
- ✅ **Reservations**: Book study rooms, reserve equipment, event registration
- ✅ **Smart Recommendations**: Personalized book suggestions
- ✅ **Rich Responses**: Visual cards, lists, quick action buttons
- ✅ **Knowledge Base**: FAQ handling with knowledge connectors
- ✅ **Multi-language Support**: Ready for internationalization
- ✅ **Error Recovery**: Graceful handling of edge cases
- ✅ **Context Awareness**: Maintains conversation context across flows

## 📁 Project Structure

```
DialogFlow/
├── README.md                          # This file
├── ARCHITECTURE.md                    # Detailed architecture documentation
├── DEPLOYMENT.md                      # Deployment guide
│
├── cloud-functions/                   # Cloud Functions for webhook fulfillment
│   ├── main.py                       # Main webhook handler
│   ├── library_service.py            # Library system integration
│   ├── utils.py                      # Utility functions
│   ├── requirements.txt              # Python dependencies
│   ├── deploy.sh                     # Deployment script
│   └── .gcloudignore                 # Files to ignore
│
├── config/                            # DialogFlow CX configurations
│   ├── flows/                        # Flow configurations
│   │   ├── main-navigation.md
│   │   ├── book-search.md
│   │   ├── account-management.md
│   │   ├── reservations.md
│   │   ├── help-faq.md
│   │   └── authentication.md
│   ├── intents/                      # Intent definitions
│   │   ├── book-search-intents.md
│   │   ├── account-intents.md
│   │   ├── reservation-intents.md
│   │   └── general-intents.md
│   ├── entities/                     # Entity definitions
│   │   ├── book-entities.md
│   │   ├── account-entities.md
│   │   └── reservation-entities.md
│   ├── knowledge-base/               # Knowledge connector setup
│   │   └── faq-setup.md
│   └── advanced-features/            # Advanced feature configs
│       ├── rich-responses.md
│       ├── conditional-routing.md
│       └── state-management.md
│
└── docs/                              # Documentation
    ├── setup-guide.md                # Complete setup instructions
    ├── testing-guide.md               # Comprehensive testing
    ├── user-experience.md            # UX design principles
    └── troubleshooting.md            # Common issues and solutions
```

## 🚀 Quick Start

### Prerequisites

- Google Cloud Platform account with billing enabled
- DialogFlow CX API enabled
- Cloud Functions API enabled
- Library system API access (or mock data for testing)

### Deployment Steps

1. **Deploy Cloud Functions**:
   ```bash
   cd cloud-functions
   ./deploy.sh
   ```

2. **Create DialogFlow CX Agent**:
   - Follow `docs/setup-guide.md` for detailed instructions

3. **Configure Flows**:
   - Set up all flows as documented in `config/flows/`

4. **Set Up Knowledge Base**:
   - Configure knowledge connectors as per `config/knowledge-base/`

5. **Test and Iterate**:
   - Use comprehensive testing guide in `docs/testing-guide.md`

## 🎨 Advanced Features Demonstrated

### 1. Multiple Flows with Transitions
- Specialized flows for different domains
- Smooth transitions between flows
- Context preservation across flows

### 2. Rich Responses
- **Cards**: Book information with images
- **Lists**: Search results, account items
- **Quick Replies**: Action buttons for common tasks
- **Images**: Book covers, library maps

### 3. Knowledge Connectors
- FAQ handling via knowledge base
- Automatic answer extraction
- Fallback to human agent when needed

### 4. Advanced Entity Extraction
- Composite entities (book titles with authors)
- System entities (@sys.date, @sys.time, @sys.number)
- Custom entities with synonyms and fuzzy matching

### 5. Conditional Logic
- Dynamic responses based on user data
- Conditional routing based on account status
- Personalized recommendations

### 6. State Management
- Session variables for user context
- Form state management
- Multi-step processes

### 7. Error Recovery
- Graceful handling of API failures
- User-friendly error messages
- Retry mechanisms
- Fallback responses

## 📚 Documentation

- **ARCHITECTURE.md**: Detailed system architecture
- **DEPLOYMENT.md**: Step-by-step deployment guide
- **docs/setup-guide.md**: Complete setup instructions
- **docs/testing-guide.md**: Testing procedures
- **docs/user-experience.md**: UX design principles

## 🔧 Technologies Used

- **DialogFlow CX**: Conversational AI platform
- **Cloud Functions (Gen2)**: Webhook fulfillment
- **Python 3.11**: Backend logic
- **OpenAPI/REST**: Library system integration
- **Knowledge Connectors**: FAQ handling

## 🎯 Use Cases Covered

1. **Book Discovery**: Search, browse, recommendations
2. **Account Management**: Checkouts, holds, renewals
3. **Resource Booking**: Study rooms, equipment
4. **Information Retrieval**: Hours, policies, FAQs
5. **User Support**: Help, troubleshooting, guidance

## 📊 Key Metrics

- **Flows**: 6 specialized flows
- **Intents**: 25+ intents across all flows
- **Entities**: 15+ custom entities
- **Pages**: 30+ pages with complex routing
- **Webhook Endpoints**: 10+ integration points

## 🔒 Security & Privacy

- User authentication flow
- Secure API communication
- Data privacy compliance
- Session management

## 🤝 Contributing

This is a professional demonstration project showcasing advanced DialogFlow CX capabilities. Use it as a reference for building production-grade conversational agents.

## 📝 License

This project is for educational and demonstration purposes.

---

**Built with ❤️ using DialogFlow CX Advanced Features**
