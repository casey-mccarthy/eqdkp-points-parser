"""
Application configuration module.
"""
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv, set_key
from pathlib import Path

@dataclass
class AppConfig:
    """Application configuration settings."""
    
    api_key: Optional[str]
    xml_output_file: str = "response.xml"
    csv_output_file: str = "processed_data.csv"
    log_directory: str = "logs"

    @classmethod
    def load(cls) -> 'AppConfig':
        """
        Load and validate configuration from environment variables.
        
        Returns:
            AppConfig instance with loaded settings
        """
        load_dotenv()
        
        api_key = os.getenv('API_KEY')

        if not api_key:
            print("Missing environment variable: API_KEY")
            cls.prompt_for_missing_vars(['API_KEY'])
            return cls.load()  # Retry loading after setting missing variables
        
        return cls(api_key=api_key)

    @staticmethod
    def prompt_for_missing_vars(missing_vars: list) -> None:
        """
        Prompt the user to input missing environment variables and save them to the .env file.
        
        Args:
            missing_vars: List of missing environment variable names
        """
        env_path = Path('.env')
        if not env_path.exists():
            env_path.touch()

        for var in missing_vars:
            value = input(f"Please enter the value for {var}: ")
            set_key(env_path, var, value)
