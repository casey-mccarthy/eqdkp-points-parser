from typing import Optional
import requests
from rich.console import Console
from utils.logger import get_logger
from core.database import DatabaseManager
from core.models import Character

logger = get_logger(__name__)

class DataFetcher:
    """Handles fetching data from the EQDKP API."""
    
    def __init__(self) -> None:
        """Initialize the DataFetcher."""
        self.console = Console()
        self.base_url = "https://dkp.kwsm.app/api.php"
        self.db_manager = DatabaseManager()

    def fetch_character_data(self, api_token: str) -> Optional[str]:
        """
        Fetch points data from the API and return the XML data.
        
        Args:
            api_token: The API token for authentication
        
        Returns:
            The raw XML data as a string, or None if the request fails.
        """
        logger.info("Starting data fetch...")
        
        api_url = f"{self.base_url}?function=points&atoken={api_token}&atype=api"

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                logger.info("Data successfully fetched from the API")
                logger.debug(f"Response content type: {type(response.text)}")
                logger.debug(f"First 200 characters of response: {response.text[:200]}")
                return response.text  # Ensure this is being handled correctly
            else:
                logger.error(f"Failed to fetch data. Status: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None

    def debug_response(self, response: requests.Response, file_path: str) -> None:
        """
        Debug helper to validate API response and saved XML file.
        
        Args:
            response: The API response object
            file_path: Path where XML file is saved
        """
        # Check API Response
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"First 200 characters of response: {response.text[:200]}")
        
        # Check saved file
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                logger.debug(f"Saved file exists: True")
                logger.debug(f"File size: {len(content)} bytes")
                logger.debug(f"First 200 characters of file: {content[:200]}")
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error reading file: {e}")
