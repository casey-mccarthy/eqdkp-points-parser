"""
Main entry point for the EQDKP Parser application.
"""
from typing import NoReturn
import sys

from app.config import AppConfig
from core.data_fetcher import DataFetcher
from core.data_parser import DataParser
from core.data_processor import DataProcessor
from interface.cli import CLI
from utils.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

class EQDKPParserApp:
    """Main application class that orchestrates the EQDKP Parser functionality."""
    
    def __init__(self) -> None:
        """Initialize application components and configuration."""
        self.config = AppConfig.load()
        self.data_fetcher = DataFetcher()
        self.data_parser = DataParser()
        self.data_processor = DataProcessor()
        self.cli = None  # Initialize CLI after data processing
        
        logger.info("Application initialized")

    def run(self) -> NoReturn:
        """
        Run the main application loop.
        
        This method orchestrates the main application flow:
        1. Validates configuration
        2. Fetches data from API
        3. Parses and processes the data
        4. Starts the CLI interface
        """
        try:
            self._validate_config()
            processed_data = self._fetch_and_process_data()
            self.cli = CLI(processed_data)
            self.cli.start()
            
        except Exception as e:
            logger.error(f"Application error: {e}")
            if self.cli:
                self.cli.console.print(f"[bold red]Fatal error: {e}[/bold red]")
            else:
                print(f"Fatal error: {e}")
            sys.exit(1)

    def _validate_config(self) -> None:
        """Validate required configuration settings."""
        if not self.config.api_key:
            raise ValueError("API key not found in environment variables")
        logger.info("Configuration validated")

    def _fetch_and_process_data(self) -> pd.DataFrame:
        """
        Fetch, parse, and process the DKP data.
        
        Returns:
            pd.DataFrame: Processed data frame
        
        Raises:
            RuntimeError: If any step in the data pipeline fails
        """
        try:
            # Fetch XML data
            xml_file = self.data_fetcher.fetch_data(
                self.config.api_key,
                self.config.xml_output_file
            )
            if not xml_file:
                raise RuntimeError("Failed to fetch data from API")

            # Parse XML data
            parsed_data = self.data_parser.parse_xml(xml_file)
            if not parsed_data:
                raise RuntimeError("Failed to parse XML data")

            # Process data
            processed_data = self.data_processor.process_data(
                parsed_data,
                self.config.csv_output_file
            )
            if processed_data.empty:
                raise RuntimeError("No data processed")

            logger.info("Data fetching and processing completed successfully")
            return processed_data

        except Exception as e:
            logger.error(f"Data pipeline error: {str(e)}")
            raise RuntimeError(f"Data pipeline failed: {str(e)}")

def main() -> None:
    """Application entry point."""
    app = EQDKPParserApp()
    app.run()

if __name__ == "__main__":
    main()
