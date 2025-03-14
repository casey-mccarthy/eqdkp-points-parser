"""
Main entry point for the EQDKP Parser application.
"""
from typing import NoReturn
import sys
import os
import pyfiglet

from app.config import AppConfig
from core.data_fetcher import DataFetcher
from interface.cli import CLI
from utils.logger import get_logger
from utils.progress import ProgressManager
from rich.console import Console
from core.database import DatabaseManager
from core.data_parser import DataParser

logger = get_logger(__name__)

class EQDKPParserApp:
    """Main application class that orchestrates the EQDKP Parser functionality."""
    
    def __init__(self) -> None:
        """Initialize application components and configuration."""
        self.config = AppConfig.load()
        self.data_fetcher = DataFetcher()
        self.data_parser = DataParser()
        self.progress = ProgressManager()
        self.console = Console()
        self.cli = None
        self.db_manager = DatabaseManager()
        
        logger.info("Application initialized")

    def run(self) -> NoReturn:
        """
        Run the main application loop.
        
        This method orchestrates the main application flow:
        1. Validates configuration
        2. Fetches data from API
        3. Processes the data
        4. Starts the CLI interface
        """
        try:
            # Display header first
            ascii_art = pyfiglet.figlet_format("EQDKP Parser", font="slant")
            self.console.print(f"[bold cyan]{ascii_art}[/bold cyan]")
            
            self._fetch_character_data()
            self._fetch_ranks_data()
            self.cli = CLI()
            self.cli.start()
            
        except Exception as e:
            logger.error(f"Application error: {e}")
            if self.cli:
                self.cli.console.print(f"[bold red]Fatal error: {e}[/bold red]")
            else:
                print(f"Fatal error: {e}")
            sys.exit(1)


    def _fetch_character_data(self) -> None:
        """Fetch character data from the API and update the local list of characters."""
        self.progress.show_progress("Fetching character data from API...", success=False)
        character_data = self.data_fetcher.fetch_character_data(self.config.api_key)

        # Parse the XML data and save to database
        try:    
            self.progress.show_progress("Parsing character data...", success=False)
            self.data_parser.parse_character_data(character_data)

        except Exception as e:
            self.progress.show_progress("Error parsing XML data", success=False)
            logger.error(f"Error parsing XML data: {e}")
            return
        
        self.progress.show_progress("Character data successfully fetched and updated")

    def _fetch_ranks_data(self) -> None:
        """Fetch ranks data from the API and update the local list of ranks."""
        self.progress.show_progress("Fetching ranks data from API...", success=False)
        ranks_data = self.data_fetcher.fetch_ranks_data(self.config.api_key)
        self.data_parser.parse_character_rank_data(ranks_data)
        self.progress.show_progress("Ranks data successfully fetched and updated")  

def main(debug: bool = False) -> None:
    """
    Application entry point.
    
    Args:
        debug: Enable debug output if True
    """
    # Set debug mode environment variable
    os.environ['DEBUG_MODE'] = 'true' if debug else 'false'
    
    app = EQDKPParserApp()
    app.run()

if __name__ == "__main__":
    main()
