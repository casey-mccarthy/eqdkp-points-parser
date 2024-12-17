from typing import List
import pandas as pd
from rich.console import Console
from rich.table import Table

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
        # Check if the character is already in the current bid
        if any(char['main_character'].lower() == character_name.lower() for char in self.current_bid):
            self.console.print(f"[yellow]Character '{character_name}' is already in the bid![/yellow]")
            return

        character = self.character_data[self.character_data['main_character'].str.lower() == character_name.lower()]
        if not character.empty:
            self.current_bid.append(character.iloc[0])
            self.console.print(f"[cyan]Added {character_name} to the bid.[/cyan]")
            self.display_sorted_bid()
        else:
            self.console.print(f"[red]Character '{character_name}' not found![/red]")

    def display_sorted_bid(self) -> None:
        """Display the current bid participants sorted by points."""
        sorted_bid = sorted(self.current_bid, key=lambda x: x['points_current'], reverse=True)
        table = Table(title="Current Bid Participants")
        table.add_column("Main Character", style="magenta")
        table.add_column("Current Points", justify="right", style="red")

        for index, char in enumerate(sorted_bid):
            style = "green" if index == 0 else None  # Highlight the top character in green
            table.add_row(char['main_character'], str(char['points_current']), style=style)

        self.console.print(table)

    def end_bid(self) -> None:
        """End the current bidding session."""
        self.console.print("[yellow]Bidding session ended![/yellow]")
        self.display_sorted_bid()
        self.current_bid = [] 