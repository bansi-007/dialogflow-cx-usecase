"""
DialogFlow CX Webhook Handler - Library Assistant
Professional-grade webhook with advanced features for library system integration.
"""

import json
import os
import logging
from typing import Dict, Any, Optional, List
from flask import Request
from library_service import LibraryService
from utils import (
    create_rich_response,
    create_card_response,
    create_list_response,
    create_quick_reply_response,
    format_error_response,
    validate_parameters
)

# Configure logging with more detail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize library service
library_service = LibraryService()


def handle_webhook(request: Request) -> Dict[str, Any]:
    """
    Main webhook handler for DialogFlow CX fulfillment.
    Routes requests to appropriate handlers based on intent and flow.
    
    Args:
        request: Flask request object from Cloud Functions
        
    Returns:
        JSON response compatible with DialogFlow CX webhook format
    """
    try:
        request_json = request.get_json(silent=True)
        
        logger.info("=" * 50)
        logger.info("WEBHOOK REQUEST RECEIVED")
        logger.info("=" * 50)
        logger.info(f"Full request JSON: {json.dumps(request_json, indent=2)}")
        
        if not request_json:
            logger.error("Invalid request format: No JSON body")
            return format_error_response("Invalid request format")
        
        # Extract request information
        session_info = request_json.get('sessionInfo', {})
        intent_info = request_json.get('intentInfo', {})
        page_info = request_json.get('pageInfo', {})
        
        logger.info(f"Session Info: {json.dumps(session_info, indent=2)}")
        logger.info(f"Intent Info: {json.dumps(intent_info, indent=2)}")
        logger.info(f"Page Info: {json.dumps(page_info, indent=2)}")
        
        intent_name = intent_info.get('displayName', '') if isinstance(intent_info, dict) else ''
        
        # Safely extract flow and page names
        current_flow = page_info.get('currentFlow', {}) if isinstance(page_info, dict) else {}
        current_page = page_info.get('currentPage', {}) if isinstance(page_info, dict) else {}
        
        flow_name = current_flow.get('displayName', '') if isinstance(current_flow, dict) else ''
        page_name = current_page.get('displayName', '') if isinstance(current_page, dict) else ''
        
        # Extract parameters
        parameters = session_info.get('parameters', {})
        
        # Extract fulfillment tag
        fulfillment_info = request_json.get('fulfillmentInfo', {})
        tag = fulfillment_info.get('tag', '')
        
        logger.info(f"Extracted - Flow: {flow_name}, Page: {page_name}, Intent: {intent_name}, Tag: {tag}")
        logger.info(f"Extracted Parameters: {json.dumps(parameters, indent=2)}")
        
        # Route based on flow and intent
        logger.info("Routing request to handler...")
        response = route_request(flow_name, page_name, intent_name, parameters, session_info, tag)
        logger.info(f"Handler Response: {json.dumps(response, indent=2)}")
        
        # Build DialogFlow CX response
        final_response = build_response(response, session_info)
        logger.info(f"Final Response to DialogFlow: {json.dumps(final_response, indent=2)}")
        logger.info("=" * 50)
        
        return final_response
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return format_error_response(f"An error occurred: {str(e)}")


def route_request(
    flow_name: str,
    page_name: str,
    intent_name: str,
    parameters: Dict[str, Any],
    session_info: Dict[str, Any],
    tag: str = ''
) -> Dict[str, Any]:
    """
    Route request to appropriate handler based on flow, intent, and tag.
    
    Args:
        flow_name: Current flow name
        page_name: Current page name
        intent_name: Matched intent name
        parameters: Extracted parameters
        session_info: Session information
        tag: Webhook tag
        
    Returns:
        Response dictionary from handler
    """
    logger.info(f"Routing logic - Flow: '{flow_name}', Intent: '{intent_name}', Tag: '{tag}'")
    
    # Priority 0: Tag-based routing (Most specific)
    if tag == 'auth-webhook' or tag == 'auth_webhook':
        return handle_authentication(parameters, session_info)
    
    # Extract user_id for account-specific tags
    user_id = session_info.get('parameters', {}).get('user_id') or parameters.get('user_id')
    
    # helper for login redirect
    # Modified to save state if present
    def create_login_redirect(tag_name):
        return {
            'message': "I need to verify your account first. Please log in to complete this action.",
            'parameters': {
                'pending_tag': tag_name,
                # Persist key parameters that might be needed
                'book_id': list(parameters.values())[0] if parameters else None, 
                # ^ crude, ideally we pass specific params. But for now session persistence usually handles the rest.
                # Actually, Dialogflow keeps session params. We just need to mark the TAG.
            },
            'redirect_to_flow': 'Authentication Flow'
        }

    if tag == 'account-checkouts':
        return handle_checkouts(user_id, parameters) if user_id else create_login_redirect('account-checkouts')
        
    if tag == 'account-renew':
        return handle_renewal(user_id, parameters) if user_id else create_login_redirect('account-renew')
        
    if tag == 'account-holds':
        return handle_holds(user_id, parameters) if user_id else create_login_redirect('account-holds')
        
    if tag == 'account-fines':
        return handle_fines(user_id, parameters) if user_id else create_login_redirect('account-fines')

    if tag == 'reservations-webhook':
        return handle_reservations(intent_name, parameters, session_info)
        
    if tag == 'book-search':
        return handle_book_search(parameters, session_info)
        
    if tag == 'get-book-details':
        return handle_book_details(parameters)
        
    if tag == 'help-faq-webhook':
        return handle_help_faq(intent_name, parameters, session_info)
    
    # Priority 1: Flow-based routing
    # If we are strictly in a specific flow, prioritize its handler
    if flow_name == "Book Search Flow":
        return handle_book_search(intent_name, parameters)
    
    elif flow_name == "Account Management Flow":
        return handle_account_management(intent_name, parameters, session_info)
        
    elif flow_name == "Reservations Flow":
        return handle_reservations(intent_name, parameters, session_info)
        
    elif flow_name == "Help & FAQ Flow":
        return handle_help_faq(intent_name, parameters, session_info)
        
    elif flow_name == "Authentication Flow":
        return handle_authentication(parameters, session_info)

    # If simple Flow match didn't catch it (e.g. entry intents), check Intents
    # Be strict to avoid overlap (e.g. "BookRoom" vs "SearchBooks")
    
    # Reservations/Booking
    if "BookRoom" == intent_name or "Reserve" in intent_name or "reservation" in intent_name.lower():
         return handle_reservations(intent_name, parameters, session_info)

    # Book Search (Check this AFTER Reservations to avoid 'BookRoom' matching 'book')
    if "SearchBooks" == intent_name or "FindBook" == intent_name or ("book" in intent_name.lower() and "room" not in intent_name.lower()):
         return handle_book_search(parameters, session_info)

    # Account
    if "Account" in intent_name or "checkout" in intent_name.lower() or "fine" in intent_name.lower():
         return handle_account_management(intent_name, parameters, session_info)

    # Help
    if "Help" in intent_name or "faq" in intent_name.lower():
         return handle_help_faq(intent_name, parameters, session_info)
         
    # Auth
    if "Login" == intent_name or "login" in intent_name.lower():
        return handle_authentication(parameters, session_info)
    
    # Default handler
    else:
        return handle_default(parameters, session_info)


def handle_book_search(parameters: Dict[str, Any], session_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle book search requests with advanced filtering.
    
    Args:
        parameters: Search parameters (title, author, genre, etc.)
        session_info: Session information
        
    Returns:
        Response dictionary with search results
    """
    try:
        logger.info("=" * 30)
        logger.info("HANDLE_BOOK_SEARCH CALLED")
        logger.info(f"Received parameters: {json.dumps(parameters, indent=2)}")
        
        # Extract search parameters
        title = parameters.get('book_title', '')
        author = parameters.get('author', '')
        isbn = parameters.get('isbn', '')
        genre = parameters.get('genre', '')
        subject = parameters.get('subject', '')
        search_type = parameters.get('search_type', 'general')
        
        logger.info(f"Extracted - Title: '{title}', Author: '{author}', ISBN: '{isbn}', Genre: '{genre}', Subject: '{subject}'")
        
        # Validate parameters
        if not any([title, author, isbn, genre, subject]):
            logger.info("No search parameters provided, returning prompt message")
            return {
                'message': "I'd be happy to help you search for books! What would you like to search for? You can search by title, author, ISBN, genre, or subject.",
                'parameters': {},
                'suggestions': ['Search by title', 'Search by author', 'Browse by genre']
            }
        
        # Perform search
        logger.info(f"Calling library_service.search_books with title='{title}'")
        search_results = library_service.search_books(
            title=title,
            author=author,
            isbn=isbn,
            genre=genre,
            subject=subject
        )
        logger.info(f"Search returned {len(search_results) if search_results else 0} results")
        
        if not search_results:
            return {
                'message': f"I couldn't find any books matching your search. Would you like to try a different search term?",
                'parameters': {},
                'suggestions': ['Try different keywords', 'Browse by genre', 'Get recommendations']
            }
        
        # Format results based on count
        if len(search_results) == 1:
            # Single result - show detailed card
            book = search_results[0]
            return {
                'message': f"I found a book matching your search:",
                'rich_response': create_card_response(
                    title=book.get('title', 'Unknown'),
                    subtitle=f"By {book.get('author', 'Unknown Author')}",
                    text=f"ISBN: {book.get('isbn', 'N/A')}\nGenre: {book.get('genre', 'N/A')}\nStatus: {book.get('availability', 'Unknown')}",
                    image_url=book.get('cover_image', ''),
                    buttons=[
                        {'text': 'Place Hold', 'postback': f"place_hold_{book.get('id')}"},
                        {'text': 'View Details', 'postback': f"details_{book.get('id')}"}
                    ]
                ),
                'parameters': {'search_results': search_results}
            }
        else:
            # Multiple results - show list
            return {
                'message': f"I found {len(search_results)} books matching your search:",
                'rich_response': create_list_response(
                    items=search_results[:10],  # Limit to 10 items
                    title_key='title',
                    description_key='author',
                    image_key='cover_image'
                ),
                'parameters': {'search_results': search_results},
                'suggestions': ['Show more results', 'Refine search', 'Get recommendations']
            }
            
    except Exception as e:
        logger.error(f"Error in book search: {str(e)}")
        return {
            'message': "I'm having trouble searching the catalog right now. Please try again in a moment.",
            'parameters': {}
        }


def handle_account_management(
    intent_name: str,
    parameters: Dict[str, Any],
    session_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Handle account management requests (checkouts, renewals, holds, fines).
    
    Args:
        intent_name: Detected intent name
        parameters: Request parameters
        session_info: Session information
        
    Returns:
        Response dictionary
    """
    try:
        user_id = session_info.get('parameters', {}).get('user_id') or parameters.get('user_id')
        
        if not user_id:
            return {
                'message': "I need to verify your account first. Please log in to access your account information.",
                'parameters': {},
                'redirect_to_flow': 'Authentication Flow'
            }
        
        # Route based on intent
        if 'checkout' in intent_name.lower() or 'borrowed' in intent_name.lower():
            return handle_checkouts(user_id, parameters)
        elif 'renew' in intent_name.lower():
            return handle_renewal(user_id, parameters)
        elif 'hold' in intent_name.lower():
            return handle_holds(user_id, parameters)
        elif 'fine' in intent_name.lower() or 'fee' in intent_name.lower():
            return handle_fines(user_id, parameters)
        elif 'account' in intent_name.lower() or 'profile' in intent_name.lower():
            return handle_account_info(user_id, parameters)
        else:
            return {
                'message': "I can help you with checkouts, renewals, holds, and fines. What would you like to do?",
                'parameters': {},
                'suggestions': ['View checkouts', 'Renew books', 'View holds', 'Pay fines']
            }
            
    except Exception as e:
        logger.error(f"Error in account management: {str(e)}")
        return {
            'message': "I'm having trouble accessing your account information. Please try again later.",
            'parameters': {}
        }


def handle_book_details(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Handle request for specific book details (e.g. from list selection)."""
    try:
        # Dialogflow sends 'selected_item_id' in list events
        book_id = parameters.get('selected_item_id')
        if not book_id:
             return {'message': "I couldn't identify which book you selected.", 'parameters': {}}

        # In a real app, we'd fetch specific ID.
        # For mock, search_books returns list with IDs, we can't search by ID directly yet in 'search_books' 
        # but let's assume get_book_details in library_service works or we add it. 
        # Actually library_service has get_book_details(book_id).
        
        book = library_service.get_book_details(book_id)
        if not book:
            # Fallback if ID lookup fails (or mock doesn't match)
            return {'message': "I couldn't find details for that book.", 'parameters': {}}

        return {
            'message': f"Here are the details for '{book.get('title')}':",
            'rich_response': create_card_response(
                title=book.get('title', 'Unknown'),
                subtitle=f"By {book.get('author', 'Unknown Author')}",
                text=f"ISBN: {book.get('isbn', 'N/A')}\nGenre: {book.get('genre', 'N/A')}\nAvailability: {book.get('availability', 'Unknown')}",
                image_url=book.get('cover_image', ''),
                buttons=[
                    # IMPORTANT: passing the TITLE so PlaceHold intent can pick it up if they click or say it
                    {'text': f"Place Hold on {book.get('title')}", 'postback': f"Place a hold on {book.get('title')}"}
                ]
            ),
             # We set 'book_title' param so context carries over if they just say "Place a hold"
            'parameters': {'book_title': book.get('title'), 'book_id': book.get('id')}
        }
    except Exception as e:
        logger.error(f"Error getting book details: {str(e)}")
        return {'message': "Error retrieving book details.", 'parameters': {}}


def handle_checkouts(user_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Handle viewing and managing checkouts."""
    try:
        checkouts = library_service.get_checkouts(user_id)
        
        if not checkouts:
            return {
                'message': "You currently have no books checked out.",
                'parameters': {'checkouts': []}
            }
        
        # Format checkouts as list
        return {
            'message': f"You have {len(checkouts)} book(s) checked out:",
            'rich_response': create_list_response(
                items=checkouts,
                title_key='title',
                description_key='due_date',
                image_key='cover_image'
            ),
            'parameters': {'checkouts': checkouts},
            'suggestions': ['Renew all', 'Renew specific book', 'View details']
        }
        
    except Exception as e:
        logger.error(f"Error getting checkouts: {str(e)}")
        return {
            'message': "I couldn't retrieve your checkouts. Please try again.",
            'parameters': {}
        }


def handle_renewal(user_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Handle book renewals."""
    try:
        book_id = parameters.get('book_id') or parameters.get('book_title')
        
        if not book_id:
            # Get all renewable books
            checkouts = library_service.get_checkouts(user_id)
            renewable = [c for c in checkouts if c.get('renewable', False)]
            
            if not renewable:
                return {
                    'message': "You don't have any books that can be renewed at this time.",
                    'parameters': {}
                }
            
            return {
                'message': f"You have {len(renewable)} book(s) that can be renewed. Which one would you like to renew?",
                'rich_response': create_list_response(
                    items=renewable,
                    title_key='title',
                    description_key='due_date'
                ),
                'parameters': {'renewable_books': renewable}
            }
        
        # Renew specific book
        result = library_service.renew_book(user_id, book_id)
        
        if result.get('success'):
            return {
                'message': f"Successfully renewed '{result.get('title')}'. New due date: {result.get('new_due_date')}",
                'parameters': {'renewal_result': result}
            }
        else:
            return {
                'message': f"I couldn't renew that book. {result.get('reason', 'Please try again later.')}",
                'parameters': {}
            }
            
    except Exception as e:
        logger.error(f"Error renewing book: {str(e)}")
        return {
            'message': "I encountered an error while renewing your book. Please try again.",
            'parameters': {}
        }


def handle_holds(user_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Handle viewing and managing holds."""
    try:
        # Determine action
        # If the user provided a book, they likely want to PLACE a hold
        # (unless we explicitly support cancelling specific books, which would need a 'cancel' action param)
        book_identifier = parameters.get('book_id') or parameters.get('book_title')
        action = parameters.get('hold_action', 'view')
        
        if book_identifier and action == 'view':
            action = 'place'
        
        if action == 'place':
            book_id = book_identifier
            if not book_id:
                return {
                    'message': "Which book would you like to place on hold?",
                    'parameters': {}
                }
            
            # Use provided hold_id if available, otherwise just place hold
            result = library_service.place_hold(user_id, book_id)
            if result.get('success'):
                # Check for smart resume context
                message = f"Successfully placed a hold on '{result.get('title')}'. You'll be notified when it's available."
                return {
                    'message': message,
                    'parameters': {'hold_result': result}
                }
            else:
                return {
                    'message': f"I couldn't place that hold. {result.get('reason', 'Please try again.')}",
                    'parameters': {}
                }
        
        # View holds
        holds = library_service.get_holds(user_id)
        
        if not holds:
            return {
                'message': "You currently have no holds.",
                'parameters': {'holds': []}
            }
        
        return {
            'message': f"You have {len(holds)} hold(s):",
            'rich_response': create_list_response(
                items=holds,
                title_key='title',
                description_key='position',
                image_key='cover_image'
            ),
            'parameters': {'holds': holds},
            'suggestions': ['Cancel hold', 'View details']
        }
        
    except Exception as e:
        logger.error(f"Error handling holds: {str(e)}")
        return {
            'message': "I'm having trouble accessing your holds. Please try again.",
            'parameters': {}
        }


def handle_fines(user_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Handle viewing and paying fines."""
    try:
        action = parameters.get('fine_action', 'view')
        
        if action == 'pay':
            fine_id = parameters.get('fine_id')
            amount = parameters.get('amount')
            
            if not fine_id or not amount:
                return {
                    'message': "I need the fine ID and amount to process payment. Which fine would you like to pay?",
                    'parameters': {}
                }
            
            result = library_service.pay_fine(user_id, fine_id, amount)
            if result.get('success'):
                return {
                    'message': f"Successfully paid ${amount:.2f}. Transaction ID: {result.get('transaction_id')}",
                    'parameters': {'payment_result': result}
                }
            else:
                return {
                    'message': f"Payment failed. {result.get('reason', 'Please try again.')}",
                    'parameters': {}
                }
        
        # View fines
        fines = library_service.get_fines(user_id)
        
        if not fines:
            return {
                'message': "You currently have no fines.",
                'parameters': {'fines': []}
            }
        
        total = sum(f.get('amount', 0) for f in fines)
        
        return {
            'message': f"You have {len(fines)} fine(s) totaling ${total:.2f}:",
            'rich_response': create_list_response(
                items=fines,
                title_key='description',
                description_key='amount',
                image_key=None
            ),
            'parameters': {'fines': fines, 'total_fines': total},
            'suggestions': ['Pay all', 'Pay specific fine', 'View details']
        }
        
    except Exception as e:
        logger.error(f"Error handling fines: {str(e)}")
        return {
            'message': "I'm having trouble accessing your fines. Please try again.",
            'parameters': {}
        }


def handle_account_info(user_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Handle account information requests."""
    try:
        account_info = library_service.get_account_info(user_id)
        
        return {
            'message': f"Here's your account information:",
            'rich_response': create_card_response(
                title=f"Account: {account_info.get('name', 'N/A')}",
                subtitle=f"Member ID: {account_info.get('member_id', 'N/A')}",
                text=f"Email: {account_info.get('email', 'N/A')}\n"
                     f"Status: {account_info.get('status', 'N/A')}\n"
                     f"Checkouts: {account_info.get('checkout_count', 0)}\n"
                     f"Holds: {account_info.get('hold_count', 0)}",
                image_url=None,
                buttons=[
                    {'text': 'View Checkouts', 'postback': 'view_checkouts'},
                    {'text': 'View Holds', 'postback': 'view_holds'},
                    {'text': 'View Fines', 'postback': 'view_fines'}
                ]
            ),
            'parameters': {'account_info': account_info}
        }
        
    except Exception as e:
        logger.error(f"Error getting account info: {str(e)}")
        return {
            'message': "I couldn't retrieve your account information. Please try again.",
            'parameters': {}
        }


def handle_reservations(intent_name: str, parameters: Dict[str, Any], session_info: Dict[str, Any]) -> Dict[str, Any]:
    """Handle reservation requests (study rooms, equipment, events)."""
    try:
        user_id = session_info.get('parameters', {}).get('user_id') or parameters.get('user_id')
        
        if not user_id:
            return {
                'message': "Please log in to make reservations.",
                'parameters': {},
                'redirect_to_flow': 'Authentication Flow'
            }
        
        reservation_type = parameters.get('reservation_type', '')
        date = parameters.get('date', '')
        time = parameters.get('time', '')
        duration = parameters.get('duration', '')
        
        if not reservation_type:
            return {
                'message': "What would you like to reserve? I can help you book study rooms, equipment, or register for events.",
                'parameters': {},
                'suggestions': ['Study room', 'Equipment', 'Event']
            }
        
        if reservation_type.lower() in ['study room', 'room']:
            return handle_study_room_booking(user_id, date, time, duration, parameters)
        elif reservation_type.lower() in ['equipment', 'device']:
            return handle_equipment_reservation(user_id, date, time, duration, parameters)
        elif reservation_type.lower() in ['event', 'program']:
            return handle_event_registration(user_id, parameters)
        else:
            return {
                'message': "I can help you reserve study rooms, equipment, or register for events. What would you like to do?",
                'parameters': {}
            }
            
    except Exception as e:
        logger.error(f"Error handling reservations: {str(e)}")
        return {
            'message': "I'm having trouble processing your reservation. Please try again.",
            'parameters': {}
        }


def handle_study_room_booking(
    user_id: str,
    date: str,
    time: str,
    duration: str,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle study room bookings."""
    try:
        if not all([date, time, duration]):
            return {
                'message': "I need a few details to book a study room. When would you like to reserve it? (date, time, and duration)",
                'parameters': {}
            }
        
        # Check availability
        available_rooms = library_service.get_available_rooms(date, time, duration)
        
        if not available_rooms:
            return {
                'message': f"Sorry, no study rooms are available for {date} at {time}. Would you like to try a different time?",
                'parameters': {},
                'suggestions': ['Try different time', 'Try different date', 'View all available times']
            }
        
        # If room specified, book it
        room_id = parameters.get('room_id')
        if room_id:
            result = library_service.book_room(user_id, room_id, date, time, duration)
            if result.get('success'):
                return {
                    'message': f"Successfully booked {result.get('room_name')} for {date} at {time}. Confirmation: {result.get('confirmation_id')}",
                    'parameters': {'booking_result': result}
                }
            else:
                return {
                    'message': f"Booking failed. {result.get('reason', 'Please try again.')}",
                    'parameters': {}
                }
        
        # Show available rooms
        return {
            'message': f"I found {len(available_rooms)} available room(s) for {date} at {time}:",
            'rich_response': create_list_response(
                items=available_rooms,
                title_key='room_name',
                description_key='capacity',
                image_key=None
            ),
            'parameters': {'available_rooms': available_rooms, 'date': date, 'time': time, 'duration': duration},
            'suggestions': ['Book room', 'View different times']
        }
        
    except Exception as e:
        logger.error(f"Error booking study room: {str(e)}")
        return {
            'message': "I encountered an error while booking the room. Please try again.",
            'parameters': {}
        }


def handle_equipment_reservation(
    user_id: str,
    date: str,
    time: str,
    duration: str,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle equipment reservations."""
    try:
        equipment_type = parameters.get('equipment_type', '')
        
        if not equipment_type:
            return {
                'message': "What type of equipment would you like to reserve? (e.g., laptop, projector, camera)",
                'parameters': {}
            }
        
        if not date:
            return {
                'message': f"When would you like to reserve the {equipment_type}?",
                'parameters': {}
            }
        
        # Check availability
        available = library_service.check_equipment_availability(equipment_type, date, duration)
        
        if not available:
            return {
                'message': f"Sorry, {equipment_type} is not available for {date}. Would you like to try a different date?",
                'parameters': {},
                'suggestions': ['Try different date', 'Try different equipment']
            }
        
        # Reserve equipment
        result = library_service.reserve_equipment(user_id, equipment_type, date, duration)
        
        if result.get('success'):
            return {
                'message': f"Successfully reserved {equipment_type} for {date}. Confirmation: {result.get('confirmation_id')}",
                'parameters': {'reservation_result': result}
            }
        else:
            return {
                'message': f"Reservation failed. {result.get('reason', 'Please try again.')}",
                'parameters': {}
            }
            
    except Exception as e:
        logger.error(f"Error reserving equipment: {str(e)}")
        return {
            'message': "I encountered an error while reserving equipment. Please try again.",
            'parameters': {}
        }


def handle_event_registration(user_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Handle event registrations."""
    try:
        event_id = parameters.get('event_id') or parameters.get('event_name')
        
        if not event_id:
            # Show available events
            events = library_service.get_upcoming_events()
            
            if not events:
                return {
                    'message': "There are no upcoming events at this time.",
                    'parameters': {}
                }
            
            return {
                'message': f"Here are upcoming events:",
                'rich_response': create_list_response(
                    items=events,
                    title_key='title',
                    description_key='date',
                    image_key='image_url'
                ),
                'parameters': {'events': events},
                'suggestions': ['Register for event', 'View event details']
            }
        
        # Register for event
        result = library_service.register_for_event(user_id, event_id)
        
        if result.get('success'):
            return {
                'message': f"Successfully registered for '{result.get('event_title')}'. Confirmation: {result.get('confirmation_id')}",
                'parameters': {'registration_result': result}
            }
        else:
            return {
                'message': f"Registration failed. {result.get('reason', 'Please try again.')}",
                'parameters': {}
            }
            
    except Exception as e:
        logger.error(f"Error registering for event: {str(e)}")
        return {
            'message': "I encountered an error while registering. Please try again.",
            'parameters': {}
        }


def handle_help_faq(intent_name: str, parameters: Dict[str, Any], session_info: Dict[str, Any]) -> Dict[str, Any]:
    """Handle help and FAQ requests."""
    try:
        query = parameters.get('help_query', '') or parameters.get('faq_query', '')
        
        if not query:
            return {
                'message': "I'm here to help! What would you like to know? I can help with library hours, policies, services, or answer general questions.",
                'parameters': {},
                'suggestions': ['Library hours', 'Borrowing policies', 'Services', 'Contact information']
            }
        
        # This would typically integrate with knowledge connector
        # For now, handle common queries
        query_lower = query.lower()
        
        if 'hour' in query_lower:
            return {
                'message': "Library Hours:\nMonday-Friday: 9:00 AM - 9:00 PM\nSaturday: 10:00 AM - 6:00 PM\nSunday: 12:00 PM - 5:00 PM",
                'parameters': {}
            }
        elif 'policy' in query_lower or 'borrow' in query_lower:
            return {
                'message': "Borrowing Policies:\n• Books: 3 weeks (2 renewals allowed)\n• DVDs: 1 week (1 renewal)\n• Maximum 20 items checked out\n• Fines: $0.25/day for overdue items",
                'parameters': {}
            }
        elif 'contact' in query_lower:
            return {
                'message': "Contact Information:\nPhone: (555) 123-4567\nEmail: library@example.com\nAddress: 123 Library Street, City, State 12345",
                'parameters': {}
            }
        else:
            return {
                'message': f"I found information about '{query}'. For more details, please visit our website or contact us directly.",
                'parameters': {},
                'suggestions': ['More information', 'Contact support', 'View website']
            }
            
    except Exception as e:
        logger.error(f"Error handling help request: {str(e)}")
        return {
            'message': "I'm having trouble finding that information. Please try rephrasing your question or contact support.",
            'parameters': {}
        }


def handle_authentication(parameters: Dict[str, Any], session_info: Dict[str, Any]) -> Dict[str, Any]:
    """Handle user authentication."""
    try:
        user_id = parameters.get('user_id') or parameters.get('member_id')
        password = parameters.get('password', '')
        
        if not user_id:
            return {
                'message': "Please provide your member ID or username to log in.",
                'parameters': {}
            }
        
        if not password:
            return {
                'message': "Please provide your password to complete login.",
                'parameters': {'user_id': user_id}
            }
        
        # Authenticate user
        result = library_service.authenticate_user(user_id, password)
        
        if result.get('success'):
            # Fetch account info immediately for seamless experience
            # We reuse the logic from handle_account_info but customize the message
            try:
                account_info = library_service.get_account_info(user_id)
                card_response = create_card_response(
                    title=f"Account: {account_info.get('name', 'N/A')}",
                    subtitle=f"Member ID: {account_info.get('member_id', 'N/A')}",
                    text=f"Email: {account_info.get('email', 'N/A')}\n"
                         f"Status: {account_info.get('status', 'N/A')}\n"
                         f"Checkouts: {account_info.get('checkout_count', 0)}\n"
                         f"Holds: {account_info.get('hold_count', 0)}",
                    image_url=None,
                    buttons=[
                        {'text': 'View Checkouts', 'postback': 'view_checkouts'},
                        {'text': 'View Holds', 'postback': 'view_holds'},
                        {'text': 'View Fines', 'postback': 'view_fines'}
                    ]
                )
                
                response = {
                    'message': f"Welcome back, {result.get('name', 'User')}! Here is your dashboard.",
                    'rich_response': card_response,
                    'parameters': {
                        'user_id': result.get('user_id'),
                        'authenticated': True,
                        'user_name': result.get('name'),
                        'login_required': None  # Explicitly clear the flag
                    },
                    'suggestions': ['Search books', 'View checkouts']
                }

                # SMART RESUME LOGIC
                # Check if there was a pending action before login
                pending_tag = parameters.get('pending_tag') or session_info.get('parameters', {}).get('pending_tag')
                if pending_tag:
                    logger.info(f"Checking smart resume for pending tag: {pending_tag}")
                    
                    # Merge session params with current params to ensure we have all context (like book_id)
                    combined_params = {**session_info.get('parameters', {}), **parameters}
                    combined_params['user_id'] = result.get('user_id') # Ensure authenticated user_id is used
                    
                    # Dispatch to the pending handler
                    if pending_tag == 'account-holds':
                        follow_up_response = handle_holds(result.get('user_id'), combined_params)
                        # Prepend a success login message to the action response
                        follow_up_response['message'] = f"Welcome back, {result.get('name', 'User')}! \n\n" + follow_up_response.get('message', '')
                        # Clear pending tag
                        follow_up_response['parameters']['pending_tag'] = None
                        return follow_up_response
                        
                    elif pending_tag == 'account-renew':
                        follow_up_response = handle_renewal(result.get('user_id'), combined_params)
                        follow_up_response['message'] = f"Welcome back, {result.get('name', 'User')}! \n\n" + follow_up_response.get('message', '')
                        follow_up_response['parameters']['pending_tag'] = None
                        return follow_up_response

                return response
            except Exception:
                # Fallback if account info fetch fails
                return {
                    'message': f"Welcome back, {result.get('name', 'User')}! How can I help you today?",
                    'parameters': {
                        'user_id': result.get('user_id'),
                        'authenticated': True,
                        'user_name': result.get('name'),
                        'login_required': None
                    },
                    'suggestions': ['View account', 'Search books', 'View checkouts']
                }
        else:
            return {
                'message': "Login failed. Please check your credentials and try again.",
                'parameters': {'authenticated': False}
            }
            
    except Exception as e:
        logger.error(f"Error authenticating: {str(e)}")
        return {
            'message': "I encountered an error during login. Please try again.",
            'parameters': {}
        }


def handle_default(parameters: Dict[str, Any], session_info: Dict[str, Any]) -> Dict[str, Any]:
    """Handle default/unrecognized requests."""
    return {
        'message': "I'm here to help you with library services. I can help you search for books, manage your account, make reservations, or answer questions. What would you like to do?",
        'parameters': {},
        'suggestions': ['Search books', 'View account', 'Make reservation', 'Get help']
    }


def build_response(response: Dict[str, Any], session_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build DialogFlow CX compatible response.
    
    Args:
        response: Response dictionary from handler
        session_info: Session information
        
    Returns:
        DialogFlow CX response format
    """
    messages = []
    
    # Add text message
    if 'message' in response:
        messages.append({
            'text': {
                'text': [response['message']]
            }
        })
    
    # Add rich response if available
    if 'rich_response' in response:
        messages.append(response['rich_response'])
    
    # Add quick replies if available
    if 'suggestions' in response:
        quick_replies = create_quick_reply_response(response['suggestions'])
        messages.append(quick_replies)
    
    # Calculate merged parameters
    final_parameters = {**session_info.get('parameters', {}), **response.get('parameters', {})}

    # Handle Redirection via Parameters (The "CX Way")
    if 'redirect_to_flow' in response and response['redirect_to_flow'] == 'Authentication Flow':
        final_parameters['login_required'] = True
    
    # Build response
    result = {
        'sessionInfo': {
            'parameters': final_parameters
        },
        'fulfillmentResponse': {
            'messages': messages
        }
    }
    
    # Add page transition if specified (Works for pages in same flow)
    # For Flow transitions, we rely on the 'login_required' parameter triggering a Route in the Console.
    if 'redirect_to_flow' in response:
        result['targetPage'] = response['redirect_to_flow']
    
    return result
