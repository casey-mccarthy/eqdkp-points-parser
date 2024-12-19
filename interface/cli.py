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
from core.bidding_manager import BiddingManager
from core.database import DatabaseManager
from rich.table import Table
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
    
    def __init__(self) -> None:
        """
        Initialize the CLI interface.
        
        Args:
            data: DataFrame containing the processed DKP data
        """
        self.console = Console()
        # add database manager
        self.db_manager = DatabaseManager()
        self.display = DisplayManager()
        self.bidding_manager = BiddingManager()
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
            "bid": Command(
                name="bid",
                description="Enter bidding mode",
                handler=self._handle_bid_mode,
                shorthand="b"
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
        """Display welcome message and command help."""
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
                self.console.print("\n[yellow]Options: character <name> or c <name>, "
                                 "top <number> or t <number>, "
                                 "bid, b, "
                                 "help or h, "
                                 "exit or e[/yellow]")
                
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
        character_name = args[0] if args else Prompt.ask("Enter character name")
        
        # Query the database for the character
        character_info = self.db_manager.get_character_by_name(character_name)
        
        if character_info:
            # Display character information
            table = Table(title=f"Character: {character_info.name}")
            table.add_column("Attribute", style="magenta")
            table.add_column("Value", style="cyan")
      
            
            table.add_row("ID", str(character_info.id))
            table.add_row("Name", character_info.name)
            table.add_row("Class", character_info.class_name)
            table.add_row("Rank", character_info.rank_name or "N/A")
            table.add_row("MMBz (C)", str(character_info.points.current_with_twink), style="green")
            table.add_row("MMBz (L)", str(character_info.points.earned_with_twink), style="yellow")

            # add all other alt characters (exclude the provided character) with this format: <name> (<class>)
            alt_characters = self.db_manager.get_all_characters(character_info.name)
            alt_characters_str = "\n".join([f"{alt.name} ({alt.rank_name})" for alt in alt_characters if alt.name != character_info.name])
            table.add_row("Alts", alt_characters_str, style="red")
            self.console.print(table)
        else:
            self.console.print(f"[bold red]Character '{character_name}' not found![/bold red]")

    def _handle_top_display(self, args: List[str]) -> None:
        """Handle top N display command."""
        try:
            count = int(args[0]) if args else IntPrompt.ask("Enter number of characters to show", default=5)
            
            # Query the database for the top N characters by points
            top_characters = self.db_manager.get_top_characters_by_points(count)
            
            if top_characters:
                # Create a rich table to display the top characters
                table = Table(title=f"Top {count} Characters by Points")
                table.add_column("Rank", style="magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Class", style="green")
                table.add_column("Current Points", justify="right", style="red")
                
                for index, character in enumerate(top_characters, start=1):
                    table.add_row(str(index), character.name, character.class_name, str(character.points.current))
                
                self.console.print(table)
            else:
                self.console.print("[red]No characters found in the database.[/red]")
        except ValueError:
            self.console.print("[red]Please provide a valid number[/red]")

    def _handle_bid_mode(self, args: List[str]) -> None:
        """Enter bidding mode."""
        self.bidding_manager.start_bid()
        while True:
            command = Prompt.ask("[bold cyan]Enter character name to add or 'end'/'e' to finish bidding[/bold cyan]")
            if command.lower() in ['end', 'e']:
                self.bidding_manager.end_bid()
                break
            else:
                self.bidding_manager.add_character(command)

    def _handle_help(self, args: List[str] = None) -> None:
        """
        Display help information with usage examples.
        
        Args:
            args: Optional list of command arguments (unused)
        """
        self.display_help()

    def display_help(self) -> None:
        """Display help information as a rich table."""
        # Define the commands and their details
        commands = [
            ("character <name> or c <name>", "Display information about a specific character."),
            ("top <number> or t <number>", "Display the top N characters by points."),
            ("bid or b", "Enter bidding mode."),
            ("exit or e", "Exit the application.")
        ]

        # Create a rich table
        table = Table(title="Help - Command List")
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Details", style="magenta")

        # Add each command and its details to the table
        for command, details in commands:
            table.add_row(command, details)

        # Print the table to the console
        self.console.print(table)

    def _handle_exit(self, args: List[str] = None) -> None:
        """
        Handle exit command.
        
        Args:
            args: Optional list of command arguments (unused)
        """
        self.console.print("[yellow]Goodbye![/yellow]")
        exit(0)
