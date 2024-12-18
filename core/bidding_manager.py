from typing import List, Optional
from rich.console import Console
from rich.table import Table
from core.database import DatabaseManager

class BiddingManager:
    """Manages bidding sessions for characters."""

    def __init__(self) -> None:
        """Initialize the bidding manager."""
        self.db_manager = DatabaseManager()
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
        # Query the database for the character
        character_info = self.db_manager.get_character_by_name(character_name)
        if character_info is not None:
            main_character = character_info.name
            character_rank = character_info.rank_name
            points_current = character_info.points.current_with_twink

            # Check if the main character is already in the current bid
            if any(char['main_character'].lower() == main_character.lower() for char in self.current_bid):
                self.console.print(f"[yellow]Character '{main_character}' is already in the bid![/yellow]")
                return

            # Add character to the current bid
            self.current_bid.append({
                'main_character': f"{main_character} ({character_rank})",
                'points_current': points_current
            })
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