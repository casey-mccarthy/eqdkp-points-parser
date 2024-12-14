import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment Variable for Base URL
BASE_URL = os.getenv("BASE_URL", "https://dkp.kwsm.app")

class APIReadPaths:
    """Holds all the API paths.
    
    The paths are formatted with placeholders for parameters that need to be filled in.

    Attributes:
    USER_CHARS: Path to get the characters of the user.
    CALENDAR_EVENTS_LIST: Path to get the list of calendar events.
    CALENDAR_EVENT_DETAILS: Path to get the details of a specific calendar event.
    POINTS: Path to get the points data.
    DATA: Path to get the data.
    SEARCH_USER: Path to search for a user.
    SEARCH_CHARACTER: Path to search for a character.
    ME: Path to get the details of the authenticated user.

    Reference:
    >>> https://eqdkpplus.github.io/wiki/wiki/Plus_Exchange/Read.html
    """
    USER_CHARS = "/api.php?function=user_chars&atoken={api_token}&atype=api"
    CALENDAR_EVENTS_LIST = "/api.php?function=calevents_list&atoken={api_token}&atype=api"
    CALENDAR_EVENT_DETAILS = "/api.php?function=calevents_details&eventid={event_id}&atoken={api_token}&atype=api"
    POINTS = "/api.php?function=points&atoken={api_token}&atype=api"
    DATA = "/api.php?function=data&atoken={api_token}&atype=api"
    SEARCH_USER = "/api.php?function=search&in=username&for={username}&atoken={api_token}&atype=api"
    SEARCH_CHARACTER = "/api.php?function=search&in=charname&for={charname}&atoken={api_token}&atype=api"
    ME = "/api.php?function=me&atoken={api_token}&atype=api"

    @staticmethod
    def build_url(path: str, **params) -> str:
        """
        Construct the full URL using the base URL and the given path.
        
        :param path: Path from the APIReadPaths class.
        :param params: Parameters to format into the URL (e.g., {event_id}, {username}, {api_token}).
        :return: Full URL as a string.
        """
        return BASE_URL + path.format(**params)

def call_api(url: str, method: str = "GET", headers: dict = None, payload: dict = None):
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

def get_user_chars(api_token: str):
    url = APIReadPaths.build_url(APIReadPaths.USER_CHARS, api_token=api_token)
    return call_api(url)

def get_calendar_events_list(api_token: str, raids_only=1, number=10):
    url = APIReadPaths.build_url(APIReadPaths.CALENDAR_EVENTS_LIST, api_token=api_token) + f"&raids_only={raids_only}&number={number}"
    return call_api(url)

def get_calendar_event_details(api_token: str, event_id: int):
    url = APIReadPaths.build_url(APIReadPaths.CALENDAR_EVENT_DETAILS, api_token=api_token, event_id=event_id)
    return call_api(url)

def get_points(api_token: str, filter_type=None, filter_id=None):
    url = APIReadPaths.build_url(APIReadPaths.POINTS, api_token=api_token)
    if filter_type and filter_id:
        url += f"&filter={filter_type}&filterid={filter_id}"
    return call_api(url)

def get_data(api_token: str):
    url = APIReadPaths.build_url(APIReadPaths.DATA, api_token=api_token)
    return call_api(url)

def search_user(api_token: str, username: str):
    url = APIReadPaths.build_url(APIReadPaths.SEARCH_USER, api_token=api_token, username=username)
    return call_api(url)

def search_character(api_token: str, charname: str):
    url = APIReadPaths.build_url(APIReadPaths.SEARCH_CHARACTER, api_token=api_token, charname=charname)
    return call_api(url)

def get_me(api_token: str):
    url = APIReadPaths.build_url(APIReadPaths.ME, api_token=api_token)
    return call_api(url)
