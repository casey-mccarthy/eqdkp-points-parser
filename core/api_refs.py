import os
import requests


# Environment Variable for Base URL
BASE_URL = os.getenv("BASE_URL", "https://dkp.kwsm.app")

class APIReadPaths:
    """Holds all the API paths and provides methods to interact with them."""
    
    USER_CHARS = "/api.php?function=user_chars&atoken={api_token}&atype=api"
    CALENDAR_EVENTS_LIST = "/api.php?function=calevents_list&atoken={api_token}&atype=api"
    CALENDAR_EVENT_DETAILS = "/api.php?function=calevents_details&eventid={event_id}&atoken={api_token}&atype=api"
    POINTS = "/api.php?function=points&atoken={api_token}&atype=api"
    DATA = "/api.php?function=data&atoken={api_token}&atype=api"
    SEARCH_USER = "/api.php?function=search&in=username&for={username}&atoken={api_token}&atype=api"
    SEARCH_CHARACTER = "/api.php?function=search&in=charname&for={charname}&atoken={api_token}&atype=api"
    ME = "/api.php?function=me&atoken={api_token}&atype=api"
    RANKS = "/api.php?function=character_ranks&atoken={api_token}&atype=api"
    
    def __init__(self, api_token: str):
        """
        Initialize the APIReadPaths with an API token.
        
        :param api_token: The API token for authentication.
        """
        self.api_token = api_token

    def build_url(self, path: str, **params) -> str:
        """
        Construct the full URL using the base URL and the given path.
        
        :param path: Path from the APIReadPaths class.
        :param params: Parameters to format into the URL (e.g., {event_id}, {username}).
        :return: Full URL as a string.
        """
        return BASE_URL + path.format(api_token=self.api_token, **params)

    def call_api(self, url: str, method: str = "GET", headers: dict = None, payload: dict = None):
        """
        Central method to make API calls.
        
        :param url: The complete URL to call.
        :param method: HTTP method (GET, POST, etc.).
        :param headers: Additional headers if required.
        :param payload: JSON payload for POST requests.
        :return: Parsed response if successful, raises an exception otherwise.
        """
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=payload)
            else:
                raise ValueError("Unsupported HTTP method.")

            response.raise_for_status()
            return response.json() if 'application/json' in response.headers.get('Content-Type', '') else response.text

        except requests.exceptions.RequestException as e:
            raise Exception(f"API call to {url} failed: {str(e)}") from e

    def get_user_chars(self):
        """Get the characters of the user."""
        url = self.build_url(self.USER_CHARS)
        return self.call_api(url)

    def get_calendar_events_list(self, raids_only: int = 1, number: int = 10):
        """Get the list of calendar events."""
        url = self.build_url(self.CALENDAR_EVENTS_LIST) + f"&raids_only={raids_only}&number={number}"
        return self.call_api(url)

    def get_calendar_event_details(self, event_id: int):
        """Get the details of a specific calendar event."""
        url = self.build_url(self.CALENDAR_EVENT_DETAILS, event_id=event_id)
        return self.call_api(url)

    def get_points(self, filter_type: str = None, filter_id: int = None):
        """Get the points data."""
        url = self.build_url(self.POINTS)
        if filter_type and filter_id:
            url += f"&filter={filter_type}&filterid={filter_id}"
        return self.call_api(url)

    def get_data(self):
        """Get the data."""
        url = self.build_url(self.DATA)
        return self.call_api(url)

    def search_user(self, username: str):
        """Search for a user."""
        url = self.build_url(self.SEARCH_USER, username=username)
        return self.call_api(url)

    def search_character(self, charname: str):
        """Search for a character."""
        url = self.build_url(self.SEARCH_CHARACTER, charname=charname)
        return self.call_api(url)

    def get_me(self):
        """Get the details of the authenticated user."""
        url = self.build_url(self.ME)
        return self.call_api(url)

    def get_ranks(self):
        """Get the character ranks."""
        url = self.build_url(self.RANKS)
        return self.call_api(url)