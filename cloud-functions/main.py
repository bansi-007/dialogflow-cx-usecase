"""
DialogFlow CX Webhook Handler
Handles fulfillment requests from DialogFlow CX and integrates with external APIs.
"""

import json
import os
import requests
from typing import Dict, Any
from flask import Request


def handle_webhook(request: Request):
    """
    Main webhook handler for DialogFlow CX fulfillment.
    
    Args:
        request: Flask request object from Cloud Functions
        
    Returns:
        JSON response compatible with DialogFlow CX webhook format
    """
    try:
        # Parse the request body
        request_json = request.get_json(silent=True)
        
        if not request_json:
            return create_error_response("Invalid request format")
        
        # Extract session info and intent
        session_info = request_json.get('sessionInfo', {})
        intent_info = request_json.get('intentInfo', {})
        intent_name = intent_info.get('displayName', '')
        
        # Extract parameters
        parameters = request_json.get('sessionInfo', {}).get('parameters', {})
        
        # Route to appropriate handler based on intent
        if intent_name == 'GetWeather':
            response = handle_weather_intent(parameters)
        elif intent_name == 'GetGreeting':
            response = handle_greeting_intent(parameters)
        elif intent_name == 'GetHelp':
            response = handle_help_intent(parameters)
        else:
            response = create_default_response()
        
        # Build DialogFlow CX webhook response
        return {
            'sessionInfo': {
                'parameters': response.get('parameters', {}),
            },
            'fulfillmentResponse': {
                'messages': [
                    {
                        'text': {
                            'text': [response.get('message', 'I received your request.')]
                        }
                    }
                ]
            }
        }
        
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return create_error_response(f"An error occurred: {str(e)}")


def handle_weather_intent(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle weather-related queries using OpenWeatherMap API.
    
    Args:
        parameters: Extracted parameters from DialogFlow CX
        
    Returns:
        Response dictionary with message and parameters
    """
    city = parameters.get('city', '')
    api_key = os.environ.get('OPENWEATHER_API_KEY', '')
    
    if not city:
        return {
            'message': 'I need to know which city you want weather information for. Please specify a city name.',
            'parameters': {}
        }
    
    if not api_key:
        return {
            'message': 'Weather service is currently unavailable. Please try again later.',
            'parameters': {}
        }
    
    try:
        # Call OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'  # Use metric units (Celsius)
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract weather information
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        feels_like = data['main']['feels_like']
        
        # Format response message
        message = (
            f"The weather in {city} is currently {description}. "
            f"The temperature is {temperature:.1f}°C (feels like {feels_like:.1f}°C). "
            f"Humidity is {humidity}%."
        )
        
        return {
            'message': message,
            'parameters': {
                'temperature': temperature,
                'description': description,
                'humidity': humidity,
                'city': city
            }
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Weather API error: {str(e)}")
        return {
            'message': f"Sorry, I couldn't fetch weather information for {city}. Please check if the city name is correct and try again.",
            'parameters': {}
        }
    except KeyError as e:
        print(f"Error parsing weather data: {str(e)}")
        return {
            'message': 'I received weather data but had trouble processing it. Please try again.',
            'parameters': {}
        }


def handle_greeting_intent(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle greeting intents with personalized responses.
    
    Args:
        parameters: Extracted parameters from DialogFlow CX
        
    Returns:
        Response dictionary with greeting message
    """
    name = parameters.get('name', '')
    
    if name:
        message = f"Hello {name}! How can I help you today? I can provide weather information, answer questions, or help with various tasks."
    else:
        message = "Hello! How can I help you today? I can provide weather information, answer questions, or help with various tasks."
    
    return {
        'message': message,
        'parameters': {}
    }


def handle_help_intent(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle help requests with information about available features.
    
    Args:
        parameters: Extracted parameters from DialogFlow CX
        
    Returns:
        Response dictionary with help message
    """
    message = (
        "I'm here to help! Here's what I can do:\n\n"
        "🌤️ **Weather Information**: Ask me about the weather in any city. "
        "For example: 'What's the weather in New York?'\n\n"
        "👋 **Greetings**: I can greet you and have a friendly conversation.\n\n"
        "❓ **General Questions**: Feel free to ask me anything, and I'll do my best to help.\n\n"
        "Just tell me what you need, and I'll assist you!"
    )
    
    return {
        'message': message,
        'parameters': {}
    }


def create_default_response() -> Dict[str, Any]:
    """
    Create a default response for unrecognized intents.
    
    Returns:
        Default response dictionary
    """
    return {
        'message': "I understand you're trying to communicate with me. Could you please rephrase your request? I can help with weather information, greetings, or general questions.",
        'parameters': {}
    }


def create_error_response(error_message: str) -> Dict[str, Any]:
    """
    Create an error response for DialogFlow CX.
    
    Args:
        error_message: Error message to return
        
    Returns:
        Error response dictionary
    """
    return {
        'fulfillmentResponse': {
            'messages': [
                {
                    'text': {
                        'text': [f"Sorry, I encountered an error: {error_message}"]
                    }
                }
            ]
        }
    }
