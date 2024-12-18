from typing import List
import pandas as pd
from rich.console import Console
from rich.table import Table
from utils.character_utils import find_character

class BiddingManager:
    """Manages bidding sessions for characters."""

    def __init__(self, character_data: pd.DataFrame) -> None:
        """
        Initialize the bidding manager with character data.

        Args:
            character_data: DataFrame containing character points data.
        """
        self.character_data = character_data
        self.current_bid = []
        self.console = Console()

    def start_bid(self) -> None:
        """Start a new bidding session."""
        self.current_bid = []
        self.console.print("[green]Bidding session started![/green]")

    def add_character(self, character_name: str) -> None:
        """
        Add a character to the current bid session.

        Args:
            character_name: Name of the character to add.
        """
        # Use the utility function to find the character
        character_info = find_character(self.character_data, character_name)
        if character_info is not None:
            main_character, points_current = character_info

            # Check if the main character is already in the current bid
            if any(char['main_character'].lower() == main_character.lower() for char in self.current_bid):
                self.console.print(f"[yellow]Character '{main_character}' is already in the bid![/yellow]")
                return

            # Find the row in the DataFrame to add to the bid
            row = self.character_data[
                (self.character_data['main_character'] == main_character) |
                (self.character_data['alts'].str.contains(character_name, case=False, na=False))
            ].iloc[0]
            self.current_bid.append(row)
            self.current_bid.sort(key=lambda x: x['points_current'], reverse=True)
            self.console.print(f"[cyan]Added {main_character} to the bid.[/cyan]")
            self.display_sorted_bid()
        else:
            self.console.print(f"[red]Character '{character_name}' not found![/red]")

    def display_sorted_bid(self) -> None:
        """Display the current bid participants sorted by points."""
        table = Table(title="Current Bid Participants")
        table.add_column("Main Character", style="magenta")
        table.add_column("Current Points", justify="right", style="red")

        for index, char in enumerate(self.current_bid):
            style = "green" if index == 0 else None  # Highlight the top character in green
            table.add_row(char['main_character'], str(char['points_current']), style=style)

        self.console.print(table)

    def end_bid(self) -> None:
        """End the current bidding session and announce the winner."""
        self.console.print("[yellow]Bidding session ended![/yellow]")
        self.display_sorted_bid()

        if self.current_bid:
            # The winner is the character with the highest points
            winner = self.current_bid[0]
            self.console.print(f"[bold green]Winner: {winner['main_character']} with {winner['points_current']} points![/bold green]")
        else:
            self.console.print("[red]No participants in the bid.[/red]")

        self.current_bid = [] 