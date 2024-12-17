"""
Command Line Interface module for user interaction.
"""
from typing import Dict, Any, Optional, List
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
    name: str
    description: str
    handler: callable
    shorthand: str

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
        self.commands = {
            "character": Command(
                name="character",
                description="Search for a specific character",
                handler=self._handle_character_search,
                shorthand="c"
            ),
            "top": Command(
                name="top",
                description="Show top N characters by DKP",
                handler=self._handle_top_display,
                shorthand="t"
            ),
            "help": Command(
                name="help",
                description="Show available commands",
                handler=self._handle_help,
                shorthand="h"
            ),
            "exit": Command(
                name="exit",
                description="Exit the application",
                handler=self._handle_exit,
                shorthand="e"
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
        self.console.print("[cyan]Data fetched and processed successfully![/cyan]")
        self._handle_help()

    def _check_environment(self) -> None:
        """Check if required environment variables are set."""
        if not os.getenv('API_KEY_CORE_READ'):
            logger.warning("API key not found in environment")
            self.console.print("[bold red]Warning: API key not found in environment[/bold red]")

    def _command_loop(self) -> None:
        """Main command processing loop."""
        while True:
            try:
                # Show available commands on each loop in yellow
                self.console.print("\n[yellow dim]Available commands: character/c, top/t, help/h, exit/e[/yellow dim]")
                
                user_input = Prompt.ask("\nEnter command").lower().split()
                if not user_input:
                    continue

                command = user_input[0]
                args = user_input[1:] if len(user_input) > 1 else []

                # Check for both full command and shorthand
                cmd_obj = next(
                    (cmd for cmd in self.commands.values() 
                     if command in [cmd.name, cmd.shorthand]),
                    None
                )

                if cmd_obj:
                    cmd_obj.handler(args)
                else:
                    self.console.print("[red]Invalid command. Type 'help' for available commands.[/red]")

            except Exception as e:
                logger.error(f"Error processing command: {e}")
                self.console.print(f"[bold red]Error: {e}[/bold red]")

    def _handle_character_search(self, args: List[str]) -> None:
        """Handle character search command."""
        if self.data is None:
            self.console.print("[bold red]No data available![/bold red]")
            return

        character = args[0] if args else Prompt.ask("Enter character name")
        self.display.display_data(self.data, character_name=character)

    def _handle_top_display(self, args: List[str]) -> None:
        """Handle top N display command."""
        if self.data is None:
            self.console.print("[bold red]No data available![/bold red]")
            return

        try:
            count = int(args[0]) if args else IntPrompt.ask("Enter number of characters to show", default=5)
            self.display.display_data(self.data, top=count)
        except ValueError:
            self.console.print("[red]Please provide a valid number[/red]")

    def _handle_help(self, args: List[str] = None) -> None:
        """
        Display help information with usage examples.
        
        Args:
            args: Optional list of command arguments (unused)
        """
        help_text = """
[bold cyan]Available Commands[/bold cyan]

[green]Search Character[/green]
  command: character, c
  usage: c dainae

[green]Show Top Characters[/green]
  command: top, t
  usage: t 10

[green]Show Help[/green]
  command: help, h

[green]Exit Application[/green]
  command: exit, e
"""
        self.console.print(help_text)

    def _handle_exit(self, args: List[str] = None) -> None:
        """
        Handle exit command.
        
        Args:
            args: Optional list of command arguments (unused)
        """
        self.console.print("[yellow]Goodbye![/yellow]")
        exit(0)
