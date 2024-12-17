from typing import Optional
import os
import requests
from rich.console import Console
from rich.progress import Progress
from utils.logger import get_logger

logger = get_logger(__name__)

class DataFetcher:
    """Handles fetching data from the EQDKP API."""
    
    def __init__(self) -> None:
        """Initialize the DataFetcher."""
        self.console = Console()
        self.base_url = "https://dkp.kwsm.app/api.php"

    def fetch_data(self, api_token: str, output_file: str = "response.xml") -> Optional[str]:
        """
        Fetch points data from the API and save to file.
        
        Args:
            api_token: The API token for authentication
            output_file: The file path to save the XML response
            
        Returns:
            str: Path to the saved XML file if successful, None otherwise
        """
        logger.info("Starting data fetch...")
        
        api_url = f"{self.base_url}?function=points&atoken={api_token}&atype=api"

        try:
            with Progress(console=self.console, transient=True) as progress:
                task = progress.add_task("[cyan]Fetching points data...", total=100)
                response = requests.get(api_url)
                progress.update(task, completed=100)

            if response.status_code == 200:
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(response.text)
                logger.info(f"Data successfully saved to {output_file}")
                return output_file
            else:
                error_msg = f"Failed to fetch data. Status: {response.status_code}"
                logger.error(error_msg)
                self.console.print(f"[bold red]{error_msg}[/bold red]")
                return None

        except Exception as e:
            error_msg = f"An error occurred: {e}"
            logger.error(error_msg)
            self.console.print(f"[bold red]{error_msg}[/bold red]")
            return None
