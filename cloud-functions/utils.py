"""
Utility functions for DialogFlow CX webhook responses.
Handles rich response formatting and validation.
"""

from typing import Dict, Any, List, Optional


def create_rich_response(response_type: str, **kwargs) -> Dict[str, Any]:
    """
    Create a rich response for DialogFlow CX.
    
    Args:
        response_type: Type of rich response (card, list, etc.)
        **kwargs: Response-specific parameters
        
    Returns:
        Rich response dictionary
    """
    if response_type == 'card':
        return create_card_response(**kwargs)
    elif response_type == 'list':
        return create_list_response(**kwargs)
    elif response_type == 'quick_reply':
        return create_quick_reply_response(**kwargs)
    else:
        return {}


def create_card_response(
    title: str,
    subtitle: Optional[str] = None,
    text: Optional[str] = None,
    image_url: Optional[str] = None,
    buttons: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Create a card response (Info Card) for DialogFlow CX (Messenger format).
    """
    rich_element = {
        'type': 'info',
        'title': title
    }
    
    if subtitle:
        rich_element['subtitle'] = subtitle
    elif text:
        rich_element['subtitle'] = text
        
    if image_url:
        rich_element['image'] = {
            'src': {
                'rawUrl': image_url
            }
        }
        
    if buttons and len(buttons) > 0:
        # Note: 'info' type usually supports one actionLink. 
        # For multiple buttons, we would need 'chips' or standard buttons below.
        # Here we will just take the first button as the actionLink if available
        # OR better: use 'description' type with a button, but let's stick to 'info' for the main card
        # and maybe append chips for actions.
        rich_element['actionLink'] = buttons[0].get('postback', '#')
    
    # We wrap this in a custom payload
    return {
        'payload': {
            'richContent': [
                [rich_element]
            ]
        }
    }


def create_list_response(
    items: List[Dict[str, Any]],
    title_key: str = 'title',
    description_key: str = 'description',
    image_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a list response for DialogFlow CX (Messenger format).
    """
    rich_content_list = []
    
    for item in items[:5]:  # Limit to 5 items for cleaner UI
        list_element = {
            'type': 'list',
            'title': str(item.get(title_key, 'Unknown')),
            'subtitle': str(item.get(description_key, ''))
        }
        
        # Add event/postback trigger when clicked
        list_element['event'] = {
            'name': 'SELECT_ITEM',
            'languageCode': 'en',
            'parameters': {'selected_item_id': str(item.get('id', ''))}
        }
        
        if image_key and item.get(image_key):
            # Dialogflow Messenger doesn't always show images in 'list', 
            # but we can try adding it if supported or fallback to description
            pass
            
        rich_content_list.append(list_element)
        
        # Add a divider
        rich_content_list.append({'type': 'divider'})
    
    return {
        'payload': {
            'richContent': [
                rich_content_list
            ]
        }
    }


def create_quick_reply_response(suggestions: List[str]) -> Dict[str, Any]:
    """
    Create quick reply suggestions (Chips) for DialogFlow CX.
    """
    chips = []
    for suggestion in suggestions[:8]:
        chips.append({
            'text': suggestion,
            'image': {
                'src': {'rawUrl': 'https://example.com/icon.png'} # Optional icon
            } if False else None # Skip icon for now
        })
        # Clean up None values
        if chips[-1]['image'] is None:
            del chips[-1]['image']
            
    return {
        'payload': {
            'richContent': [
                [
                    {
                        'type': 'chips',
                        'options': chips
                    }
                ]
            ]
        }
    }


def format_error_response(error_message: str, user_friendly: bool = True) -> Dict[str, Any]:
    """
    Format an error response for DialogFlow CX.
    
    Args:
        error_message: Error message
        user_friendly: Whether to use user-friendly message
        
    Returns:
        Error response dictionary
    """
    if user_friendly:
        message = "I'm sorry, I encountered an issue. Please try again or contact support if the problem persists."
    else:
        message = f"Error: {error_message}"
    
    return {
        'fulfillmentResponse': {
            'messages': [
                {
                    'text': {
                        'text': [message]
                    }
                }
            ]
        }
    }


def validate_parameters(parameters: Dict[str, Any], required: List[str]) -> tuple:
    """
    Validate that required parameters are present.
    
    Args:
        parameters: Parameter dictionary
        required: List of required parameter keys
        
    Returns:
        Tuple of (is_valid, missing_parameter)
    """
    for param in required:
        if param not in parameters or not parameters[param]:
            return False, param
    
    return True, None


def format_date(date_str: str) -> str:
    """
    Format date string for display.
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        Formatted date string
    """
    # Simple date formatting - can be enhanced
    return date_str


def format_currency(amount: float) -> str:
    """
    Format currency amount for display.
    
    Args:
        amount: Currency amount
        
    Returns:
        Formatted currency string
    """
    return f"${amount:.2f}"


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'
