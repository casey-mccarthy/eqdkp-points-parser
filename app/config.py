"""
Application configuration module.
"""
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

@dataclass
class AppConfig:
    """Application configuration settings."""
    
    api_key: Optional[str]
    admin_api_key: Optional[str]
    xml_output_file: str = "response.xml"
    csv_output_file: str = "processed_data.csv"
    log_directory: str = "logs"

    @classmethod
    def load(cls) -> 'AppConfig':
        """
        Load configuration from environment variables.
        
        Returns:
            AppConfig instance with loaded settings
        """
        load_dotenv()
        
        return cls(
            api_key=os.getenv('API_KEY_CORE_READ'),
            admin_api_key=os.getenv('API_ADMIN_KEY')
        )
