# Account Management Flow Configuration

## Overview
The Account Management Flow handles all user account operations including checkouts, renewals, holds, fines, and account information.

## Flow Structure

### Account Entry Page

**Purpose**: Entry point with authentication check

**Entry Fulfillment**:
```
I can help you manage your account! I can show you:
• Your current checkouts
• Renew books
• View and manage holds
• Check and pay fines
• Account information

What would you like to do?
```

**Routes**:

1. **Route: View Checkouts**
   - **Condition**: `$intent.name == "ViewCheckouts" OR $intent.name == "MyBooks"`
   - **Target Page**: Checkouts Page
   - **Transition**: Navigate to checkouts

2. **Route: Renew Books**
   - **Condition**: `$intent.name == "RenewBook" OR $intent.name == "RenewAll"`
   - **Target Page**: Renewal Page
   - **Transition**: Navigate to renewal

3. **Route: View Holds**
   - **Condition**: `$intent.name == "ViewHolds" OR $intent.name == "MyHolds"`
   - **Target Page**: Holds Page
   - **Transition**: Navigate to holds

4. **Route: View Fines**
   - **Condition**: `$intent.name == "ViewFines" OR $intent.name == "PayFines"`
   - **Target Page**: Fines Page
   - **Transition**: Navigate to fines

5. **Route: Account Info**
   - **Condition**: `$intent.name == "ViewAccount" OR $intent.name == "AccountInfo"`
   - **Target Page**: Account Info Page
   - **Transition**: Navigate to account info

**Conditional Logic**:
- Check authentication status
- If not authenticated, redirect to Authentication Flow
- Preserve intended action for after authentication

---

### Checkouts Page

**Purpose**: Display and manage current checkouts

**Entry Fulfillment**:
- **Webhook**: Enabled
- **Webhook Tag**: checkouts-webhook

**Routes**:

1. **Route: Renew Specific Book**
   - **Condition**: `$intent.name == "RenewBook" AND $page.params.selected_book != null`
   - **Target Page**: Renewal Page
   - **Transition**: Navigate to renewal

2. **Route: Renew All**
   - **Condition**: `$intent.name == "RenewAll"`
   - **Target Page**: Renewal Confirmation Page
   - **Fulfillment**: Call webhook to renew all
   - **Transition**: Navigate to confirmation

3. **Route: View Book Details**
   - **Condition**: `$intent.name == "ViewBookDetails"`
   - **Target Flow**: Book Search Flow
   - **Transition**: Navigate to book details

**Rich Response**:
- **List Format** showing:
  - Book title and author
  - Due date (highlighted if overdue)
  - Renewal status
  - Cover image
  - Action buttons (Renew, View Details)

**Quick Replies**:
- "Renew all"
- "Renew specific book"
- "View account"

---

### Renewal Page

**Purpose**: Handle book renewals

**Form Parameters**:

1. **book_id** (Required if not pre-selected)
   - **Type**: @sys.number OR Custom Entity (@BookTitle)
   - **Prompt**: "Which book would you like to renew?"
   - **Reprompt**: "Please specify the book title or number"

2. **renew_all** (Optional)
   - **Type**: @sys.boolean
   - **Prompt**: "Would you like to renew all renewable books?"
   - **Default**: false

**Routes**:

1. **Route: Renewal Successful**
   - **Condition**: `$page.params.status == "FINAL" AND $page.params.renewal_success == true`
   - **Target Page**: Renewal Confirmation Page
   - **Fulfillment**: Call webhook to renew
   - **Transition**: Navigate to confirmation

2. **Route: Renewal Failed**
   - **Condition**: `$page.params.status == "FINAL" AND $page.params.renewal_success == false`
   - **Target Page**: Stay on page
   - **Fulfillment**: Show error message with reason

**Event Handlers**:

1. **sys.invalid-parameter**
   - **Fulfillment**: "I couldn't identify that book. Please try again or select from your checkouts."

---

### Holds Page

**Purpose**: View and manage holds

**Entry Fulfillment**:
- **Webhook**: Enabled
- **Webhook Tag**: holds-webhook

**Routes**:

1. **Route: Cancel Hold**
   - **Condition**: `$intent.name == "CancelHold"`
   - **Target Page**: Cancel Hold Confirmation Page
   - **Transition**: Navigate to cancellation

2. **Route: Modify Hold**
   - **Condition**: `$intent.name == "ModifyHold"`
   - **Target Page**: Modify Hold Page
   - **Transition**: Navigate to modification

3. **Route: Place New Hold**
   - **Condition**: `$intent.name == "PlaceHold"`
   - **Target Flow**: Book Search Flow
   - **Transition**: Navigate to book search

**Rich Response**:
- **List Format** showing:
  - Book title and author
  - Position in queue
  - Estimated availability
  - Cover image
  - Action buttons (Cancel, Modify)

---

### Fines Page

**Purpose**: View and pay fines

**Entry Fulfillment**:
- **Webhook**: Enabled
- **Webhook Tag**: fines-webhook

**Routes**:

1. **Route: Pay All Fines**
   - **Condition**: `$intent.name == "PayAllFines"`
   - **Target Page**: Payment Page
   - **Transition**: Navigate to payment

2. **Route: Pay Specific Fine**
   - **Condition**: `$intent.name == "PayFine" AND $page.params.selected_fine != null`
   - **Target Page**: Payment Page
   - **Transition**: Navigate to payment

3. **Route: View Fine Details**
   - **Condition**: `$intent.name == "ViewFineDetails"`
   - **Target Page**: Stay on page
   - **Fulfillment**: Show detailed fine information

**Rich Response**:
- **List Format** showing:
  - Fine description
  - Amount (highlighted)
  - Due date
  - Action buttons (Pay, View Details)

**Quick Replies**:
- "Pay all fines"
- "Pay specific fine"
- "View account"

---

### Payment Page

**Purpose**: Process fine payments

**Form Parameters**:

1. **fine_id** (Required if paying specific fine)
   - **Type**: @sys.number
   - **Prompt**: "Which fine would you like to pay?"
   - **Reprompt**: "Please specify the fine number"

2. **amount** (Required)
   - **Type**: @sys.number
   - **Prompt**: "How much would you like to pay?"
   - **Reprompt**: "Please specify the payment amount"

3. **payment_method** (Required)
   - **Type**: Custom Entity (@PaymentMethod)
   - **Prompt**: "How would you like to pay? Credit card, debit card, or account balance?"
   - **Reprompt**: "Please specify payment method"

**Routes**:

1. **Route: Payment Successful**
   - **Condition**: `$page.params.status == "FINAL" AND $page.params.payment_success == true`
   - **Target Page**: Payment Confirmation Page
   - **Fulfillment**: Call webhook to process payment
   - **Transition**: Navigate to confirmation

2. **Route: Payment Failed**
   - **Condition**: `$page.params.status == "FINAL" AND $page.params.payment_success == false`
   - **Target Page**: Stay on page
   - **Fulfillment**: Show error message

**Event Handlers**:

1. **sys.invalid-parameter**
   - **Fulfillment**: "I couldn't process that payment. Please check the information and try again."

---

### Account Info Page

**Purpose**: Display account information

**Entry Fulfillment**:
- **Webhook**: Enabled
- **Webhook Tag**: account-info-webhook

**Rich Response**:
- **Card Format** showing:
  - Member name and ID
  - Email address
  - Account status
  - Checkout count
  - Hold count
  - Fine total
  - Action buttons (View Checkouts, View Holds, View Fines)

**Routes**:

1. **Route: View Checkouts**
   - **Condition**: User clicks "View Checkouts" button
   - **Target Page**: Checkouts Page
   - **Transition**: Navigate to checkouts

2. **Route: View Holds**
   - **Condition**: User clicks "View Holds" button
   - **Target Page**: Holds Page
   - **Transition**: Navigate to holds

3. **Route: View Fines**
   - **Condition**: User clicks "View Fines" button
   - **Target Page**: Fines Page
   - **Transition**: Navigate to fines

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
- `checkouts`: Current checkouts data
- `holds`: Current holds data
- `fines`: Current fines data

**Authentication Requirements**:
- All pages require authentication
- Redirect to Authentication Flow if not authenticated
- Preserve intended action for after authentication

**Webhook Configuration**:
- **Webhook**: library-assistant-webhook
- **Enabled for**: All pages requiring data retrieval

---

## Advanced Features

### 1. Renewal Limits
- Check renewal eligibility
- Display renewal count
- Handle maximum renewals reached

### 2. Fine Calculations
- Show fine breakdown
- Calculate total fines
- Display payment history

### 3. Hold Management
- Show position in queue
- Estimate availability
- Allow hold modifications

### 4. Account Status
- Display account status
- Show membership expiration
- Handle account restrictions

### 5. Notifications
- Overdue reminders
- Hold available notifications
- Fine payment confirmations

---

## Testing Scenarios

1. **Authentication**: Test authentication flow
2. **View Checkouts**: Test checkout display
3. **Renewal**: Test single and bulk renewals
4. **Holds**: Test viewing and managing holds
5. **Fines**: Test viewing and paying fines
6. **Account Info**: Test account information display
7. **Error Handling**: Test API failures and edge cases
8. **Unauthenticated Access**: Test redirect to authentication
