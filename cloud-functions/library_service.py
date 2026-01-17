"""
Library Service - Integration with library system APIs
Handles all interactions with the library backend system.
"""

import os
import requests
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class LibraryService:
    """Service class for library system integration."""
    
    def __init__(self):
        """Initialize library service with API configuration."""
        self.base_url = os.environ.get('LIBRARY_API_URL', 'https://api.library.example.com')
        self.api_key = os.environ.get('LIBRARY_API_KEY', '')
        self.timeout = 10
        
        # For development/demo: use mock data if API not configured
        self.use_mock = os.environ.get('USE_MOCK_DATA', 'false').lower() == 'true'
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict[str, Any]:
        """
        Make HTTP request to library API.
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            data: Request data
            
        Returns:
            Response dictionary
        """
        if self.use_mock:
            return self._get_mock_response(endpoint, method, data)
        
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            if method == 'GET':
                response = requests.get(url, headers=headers, params=data, timeout=self.timeout)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=self.timeout)
            else:
                response = requests.delete(url, headers=headers, timeout=self.timeout)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            # Fallback to mock data on error
            return self._get_mock_response(endpoint, method, data)
    
    def search_books(
        self,
        title: str = '',
        author: str = '',
        isbn: str = '',
        genre: str = '',
        subject: str = ''
    ) -> List[Dict[str, Any]]:
        """
        Search for books in the catalog.
        
        Args:
            title: Book title
            author: Author name
            isbn: ISBN number
            genre: Genre
            subject: Subject
            
        Returns:
            List of book dictionaries
        """
        params = {}
        if title:
            params['title'] = title
        if author:
            params['author'] = author
        if isbn:
            params['isbn'] = isbn
        if genre:
            params['genre'] = genre
        if subject:
            params['subject'] = subject
        
        response = self._make_request('books/search', 'GET', params)
        return response.get('books', [])
    
    def get_book_details(self, book_id: str) -> Dict[str, Any]:
        """Get detailed information about a book."""
        response = self._make_request(f'books/{book_id}', 'GET')
        return response.get('book', {})

    # Helper to get shared mock data
    def _get_mock_books(self):
        return [
            {'id': '1', 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'isbn': '9780743273565', 'genre': 'Fiction', 'availability': 'Available', 'cover_image': 'https://example.com/gatsby.jpg'},
            {'id': '2', 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'isbn': '9780061120084', 'genre': 'Fiction', 'availability': 'Available', 'cover_image': 'https://example.com/mockingbird.jpg'},
            {'id': '3', 'title': 'Harry Potter and the Sorcerer\'s Stone', 'author': 'J.K. Rowling', 'isbn': '9780590353427', 'genre': 'Fantasy', 'availability': 'Checked Out', 'cover_image': 'https://example.com/hp1.jpg'},
            {'id': '4', 'title': 'Harry Potter and the Chamber of Secrets', 'author': 'J.K. Rowling', 'isbn': '9780439064873', 'genre': 'Fantasy', 'availability': 'Available', 'cover_image': 'https://example.com/hp2.jpg'},
            {'id': '5', 'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'isbn': '9780547928227', 'genre': 'Fantasy', 'availability': 'Available', 'cover_image': 'https://example.com/hobbit.jpg'},
            {'id': '6', 'title': '1984', 'author': 'George Orwell', 'isbn': '9780451524935', 'genre': 'Dystopian', 'availability': 'Available', 'cover_image': 'https://example.com/1984.jpg'},
            {'id': '7', 'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'isbn': '9780141439518', 'genre': 'Romance', 'availability': 'Available', 'cover_image': 'https://example.com/pride.jpg'},
            {'id': '8', 'title': 'Python Crash Course', 'author': 'Eric Matthes', 'isbn': '9781593279288', 'genre': 'Technology', 'availability': 'Available', 'cover_image': 'https://example.com/python.jpg'},
            {'id': '9', 'title': 'Introduction to Algorithms', 'author': 'Thomas H. Cormen', 'isbn': '9780262033848', 'genre': 'Technology', 'availability': 'Reference Only', 'cover_image': 'https://example.com/algo.jpg'},
            {'id': '10', 'title': 'Dune', 'author': 'Frank Herbert', 'isbn': '9780441172719', 'genre': 'Sci-Fi', 'availability': 'Checked Out', 'cover_image': 'https://example.com/dune.jpg'}
        ]
    
    def authenticate_user(self, user_id: str, password: str) -> Dict[str, Any]:
        """Authenticate user and return user information."""
        data = {
            'user_id': user_id,
            'password': password
        }
        response = self._make_request('auth/login', 'POST', data)
        return response
    
    def get_account_info(self, user_id: str) -> Dict[str, Any]:
        """Get user account information."""
        response = self._make_request(f'users/{user_id}', 'GET')
        return response.get('user', {})
    
    def get_checkouts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's current checkouts."""
        response = self._make_request(f'users/{user_id}/checkouts', 'GET')
        return response.get('checkouts', [])
    
    def renew_book(self, user_id: str, book_id: str) -> Dict[str, Any]:
        """Renew a checked-out book."""
        data = {
            'user_id': user_id,
            'book_id': book_id
        }
        response = self._make_request('checkouts/renew', 'POST', data)
        return response
    
    def get_holds(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's current holds."""
        response = self._make_request(f'users/{user_id}/holds', 'GET')
        return response.get('holds', [])
    
    def place_hold(self, user_id: str, book_id: str) -> Dict[str, Any]:
        """Place a hold on a book."""
        data = {
            'user_id': user_id,
            'book_id': book_id
        }
        response = self._make_request('holds', 'POST', data)
        return response
    
    def get_fines(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's fines."""
        response = self._make_request(f'users/{user_id}/fines', 'GET')
        return response.get('fines', [])
    
    def pay_fine(self, user_id: str, fine_id: str, amount: float) -> Dict[str, Any]:
        """Pay a fine."""
        data = {
            'user_id': user_id,
            'fine_id': fine_id,
            'amount': amount
        }
        response = self._make_request('fines/pay', 'POST', data)
        return response
    
    def get_available_rooms(self, date: str, time: str, duration: str) -> List[Dict[str, Any]]:
        """Get available study rooms for given date/time."""
        params = {
            'date': date,
            'time': time,
            'duration': duration
        }
        response = self._make_request('rooms/available', 'GET', params)
        return response.get('rooms', [])
    
    def book_room(self, user_id: str, room_id: str, date: str, time: str, duration: str) -> Dict[str, Any]:
        """Book a study room."""
        data = {
            'user_id': user_id,
            'room_id': room_id,
            'date': date,
            'time': time,
            'duration': duration
        }
        response = self._make_request('rooms/book', 'POST', data)
        return response
    
    def check_equipment_availability(self, equipment_type: str, date: str, duration: str) -> bool:
        """Check if equipment is available."""
        params = {
            'equipment_type': equipment_type,
            'date': date,
            'duration': duration
        }
        response = self._make_request('equipment/availability', 'GET', params)
        return response.get('available', False)
    
    def reserve_equipment(self, user_id: str, equipment_type: str, date: str, duration: str) -> Dict[str, Any]:
        """Reserve equipment."""
        data = {
            'user_id': user_id,
            'equipment_type': equipment_type,
            'date': date,
            'duration': duration
        }
        response = self._make_request('equipment/reserve', 'POST', data)
        return response
    
    def get_upcoming_events(self) -> List[Dict[str, Any]]:
        """Get upcoming library events."""
        response = self._make_request('events/upcoming', 'GET')
        return response.get('events', [])
    
    def register_for_event(self, user_id: str, event_id: str) -> Dict[str, Any]:
        """Register user for an event."""
        data = {
            'user_id': user_id,
            'event_id': event_id
        }
        response = self._make_request('events/register', 'POST', data)
        return response
    
    def _get_mock_response(self, endpoint: str, method: str, data: Dict = None) -> Dict[str, Any]:
        """Generate mock responses for development/testing."""
        # Mock book details
        if endpoint.startswith('books/') and 'search' not in endpoint:
            book_id = endpoint.split('/')[-1]
            all_books = self._get_mock_books()
            for book in all_books:
                if book['id'] == book_id:
                    return {'book': book}
            return {'book': {}}

        if 'books/search' in endpoint:
            # Enhanced Mock Database
            all_books = self._get_mock_books()
            
            # Simple Filter Logic
            query_title = data.get('title', '').lower()
            query_author = data.get('author', '').lower()
            query_genre = data.get('genre', '').lower()
            
            filtered_books = []
            for book in all_books:
                # If a filter is provided, check if it matches. 
                # If multiple filters are provided, strict AND match (or lenient OR, let's do lenient for demo)
                match = True
                if query_title and query_title not in book['title'].lower():
                    match = False
                if query_author and match and query_author not in book['author'].lower():
                    match = False
                if query_genre and match and query_genre not in book['genre'].lower():
                    match = False
                
                # If no filters provided, return everything (or logic to return none? usually search returns all/popular)
                if not any([query_title, query_author, query_genre]):
                    match = True
                    
                if match:
                    filtered_books.append(book)
                    
            return {'books': filtered_books}
        
        # Mock authentication
        if 'auth/login' in endpoint:
            return {
                'success': True,
                'user_id': data.get('user_id', 'user123'),
                'name': 'John Doe',
                'email': 'john.doe@example.com'
            }
        
        # Mock checkouts
        if 'checkouts' in endpoint and method == 'GET':
            return {
                'checkouts': [
                    {
                        'id': '1',
                        'book_id': '1',
                        'title': 'The Great Gatsby',
                        'due_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                        'renewable': True,
                        'cover_image': 'https://example.com/covers/gatsby.jpg'
                    }
                ]
            }
        
        # Mock holds
        if 'holds' in endpoint:
            if method == 'GET':
                return {
                    'holds': [
                        {
                            'id': '1',
                            'book_id': '2',
                            'title': 'To Kill a Mockingbird',
                            'position': 3,
                            'cover_image': 'https://example.com/covers/mockingbird.jpg'
                        }
                    ]
                }
            elif method == 'POST':
                return {
                    'success': True,
                    'hold_id': 'hold123',
                    # In our demo flow, 'book_id' often contains the title string
                    'title': data.get('book_id', 'Requested Book')
                }
        
        # Mock renewals
        if 'renew' in endpoint:
            return {
                'success': True,
                # Use the book_id/title passed in request
                'title': data.get('book_id', 'Requested Book'),
                'new_due_date': (datetime.now() + timedelta(days=21)).strftime('%Y-%m-%d')
            }
        
        # Mock rooms
        if 'rooms' in endpoint:
            if 'available' in endpoint:
                return {
                    'rooms': [
                        {
                            'id': 'room1',
                            'room_name': 'Study Room A',
                            'capacity': 4,
                            'amenities': ['Whiteboard', 'Projector']
                        },
                        {
                            'id': 'room2',
                            'room_name': 'Study Room B',
                            'capacity': 6,
                            'amenities': ['Whiteboard']
                        }
                    ]
                }
            elif 'book' in endpoint:
                return {
                    'success': True,
                    'confirmation_id': 'BOOK123',
                    'room_name': 'Study Room A'
                }
        
        # Mock equipment
        if 'equipment' in endpoint:
            if 'availability' in endpoint:
                return {'available': True}
            elif 'reserve' in endpoint:
                return {
                    'success': True,
                    'confirmation_id': 'EQ123',
                    'equipment_type': data.get('equipment_type', 'laptop')
                }
        
        # Mock events
        if 'events' in endpoint:
            if 'upcoming' in endpoint:
                return {
                    'events': [
                        {
                            'id': 'event1',
                            'title': 'Book Club Meeting',
                            'date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                            'time': '6:00 PM',
                            'image_url': 'https://example.com/events/bookclub.jpg'
                        }
                    ]
                }
            elif 'register' in endpoint:
                return {
                    'success': True,
                    'confirmation_id': 'EVENT123',
                    'event_title': 'Book Club Meeting'
                }
        
        # Mock user info
        if 'users' in endpoint and method == 'GET':
            return {
                'user': {
                    'user_id': 'user123',
                    'name': 'John Doe',
                    'email': 'john.doe@example.com',
                    'member_id': 'M123456',
                    'status': 'Active',
                    'checkout_count': 3,
                    'hold_count': 1
                }
            }
        
        # Mock fines
        if 'fines' in endpoint:
            if method == 'GET':
                return {
                    'fines': [
                        {
                            'id': 'fine1',
                            'description': 'Overdue: The Great Gatsby',
                            'amount': 2.50,
                            'due_date': '2024-01-15'
                        }
                    ]
                }
            elif 'pay' in endpoint:
                return {
                    'success': True,
                    'transaction_id': 'TXN123',
                    'amount': data.get('amount', 0)
                }
        
        # Default mock response
        return {'success': True, 'message': 'Mock response'}
