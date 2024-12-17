"""
Command Line Interface module for user interaction.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
import os
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
import pyfiglet
from interface.display import DisplayManager
from utils.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

@dataclass
class Command:
    """Represents a CLI command."""
    description: str
    handler: callable

class CLI:
    """Handles command-line interface operations."""
    
    def __init__(self, data: Optional[pd.DataFrame] = None) -> None:
        """
        Initialize the CLI interface.
        
        Args:
            data: DataFrame containing the processed DKP data
        """
        self.console = Console()
        self.data = data
        self.display = DisplayManager()
        self.commands = self._setup_commands()

    def _setup_commands(self) -> Dict[str, Command]:
        """Set up available CLI commands."""
        return {
            "character": Command(
                "Search for a specific character",
                self._handle_character_search
            ),
            "top": Command(
                "Show top N characters by DKP",
                self._handle_top_display
            ),
            "random": Command(
                "Show N random characters",
                self._handle_random_display
            ),
            "help": Command(
                "Show available commands",
                self._handle_help
            ),
            "exit": Command(
                "Exit the application",
                self._handle_exit
            )
        }

    def start(self) -> None:
        """Start the CLI interface."""
        self._display_welcome()
        self._check_environment()
        self._command_loop()

    def _display_welcome(self) -> None:
        """Display welcome message and ASCII art."""
        ascii_art = pyfiglet.figlet_format("EQDKP Parser", font="slant")
        self.console.print(f"[bold cyan]{ascii_art}[/bold cyan]")
        self.console.print("[yellow]Type 'help' to see available commands[/yellow]")

    def _check_environment(self) -> None:
        """Check if required environment variables are set."""
        if not os.getenv('API_KEY_CORE_READ'):
            logger.warning("API key not found in environment")
            self.console.print("[bold red]Warning: API key not found in environment[/bold red]")

    def _command_loop(self) -> None:
        """Main command processing loop."""
        while True:
            try:
                command = Prompt.ask("\nEnter command").lower()
                if command in self.commands:
                    self.commands[command].handler()
                else:
                    self.console.print("[red]Invalid command. Type 'help' for available commands.[/red]")
            except Exception as e:
                logger.error(f"Error processing command: {e}")
                self.console.print(f"[bold red]Error: {e}[/bold red]")

    # Command handlers
    def _handle_character_search(self) -> None:
        """Handle character search command."""
        if self.data is None:
            self.console.print("[bold red]No data available![/bold red]")
            return
        
        character = Prompt.ask("Enter character name")
        logger.debug(f"Searching for character: {character}")
        logger.debug(f"Available columns: {self.data.columns.tolist()}")
        logger.debug(f"Data sample: {self.data.head(1).to_dict('records')}")
        
        try:
            self.display.display_data(self.data, character_name=character)
        except Exception as e:
            logger.error(f"Error searching for character: {e}")
            self.console.print(f"[bold red]Error searching for character: {e}[/bold red]")

    def _handle_top_display(self) -> None:
        """Handle top N display command."""
        if self.data is None:
            self.console.print("[bold red]No data available![/bold red]")
            return
        count = IntPrompt.ask("Enter number of characters to show", default=5)
        self.display.display_data(self.data, top=count)

    def _handle_random_display(self) -> None:
        """Handle random display command."""
        if self.data is None:
            self.console.print("[bold red]No data available![/bold red]")
            return
        count = IntPrompt.ask("Enter number of random characters to show", default=5)
        self.display.display_data(self.data, random_count=count)

    def _handle_help(self) -> None:
        """Display help information."""
        self.console.print("\n[bold cyan]Available Commands:[/bold cyan]")
        for cmd, details in self.commands.items():
            self.console.print(f"[green]{cmd}[/green]: {details.description}")

    def _handle_exit(self) -> None:
        """Handle exit command."""
        self.console.print("[yellow]Goodbye![/yellow]")
        exit(0)
