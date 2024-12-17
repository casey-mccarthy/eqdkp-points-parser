"""
Display management module for rendering data in the terminal.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
import random
from rich.table import Table
from rich.console import Console
from utils.logger import get_logger
from utils.character_utils import find_character

logger = get_logger(__name__)

class DisplayManager:
    """Handles formatting and displaying data in the terminal."""
    
    def __init__(self) -> None:
        """Initialize the display manager."""
        self.console = Console()

    def display_data(self, 
                    data: pd.DataFrame, 
                    character_name: Optional[str] = None, 
                    top: Optional[int] = None) -> None:
        """
        Display DKP data based on specified filters.
        
        Args:
            data: DataFrame containing the DKP data
            character_name: Optional name to filter by
            top: Optional number of top characters to show
        """
        table = self._create_table("Aggregated DKP Points")
        
        if character_name:
            self._display_character(data, character_name, table)
        elif top:
            self._display_top(data, top, table)
        else:
            # Display all characters if no filter is specified
            self._display_top(data, len(data), table)
            
        self.console.print(table)
        logger.info("Data display completed successfully")

    def _create_table(self, title: str) -> Table:
        """Create a formatted Rich table with standard columns."""
        table = Table(title=title)
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Main Character", style="magenta")
        table.add_column("Alts", style="green")
        table.add_column("Current Points", justify="right", style="red")
        return table

    def _display_character(self, data: pd.DataFrame, character_name: str, table: Table) -> None:
        """
        Display data for a specific character.
        
        Args:
            data: DataFrame containing character data
            character_name: Name of character to search for
            table: Rich table for display
        """
        try:
            # Use the utility function to find the character
            character_info = find_character(data, character_name)
            
            if character_info is not None:
                main_character, points_current = character_info
                # Find the row in the DataFrame to add to the table
                row = data[(data['main_character'] == main_character) | 
                           (data['alts'].str.contains(character_name, case=False, na=False))].iloc[0]
                self._add_row_to_table(table, row)
                logger.info(f"Found character: {character_name}")
            else:
                # If we get here, no character was found
                logger.warning(f"Character not found: {character_name}")
                self.console.print(f"[bold red]Character '{character_name}' not found![/bold red]")
            
        except Exception as e:
            logger.error(f"Error displaying character data: {e}")
            self.console.print(f"[bold red]Error displaying character data: {e}[/bold red]")

    def _display_top(self, data: pd.DataFrame, count: int, table: Table) -> None:
        """Display top N characters by current DKP."""
        top_rows = data.nlargest(count, 'points_current')
        for _, row in top_rows.iterrows():
            self._add_row_to_table(table, row)
        logger.info(f"Displayed top {count} characters")

    def _add_row_to_table(self, table: Table, row: pd.Series) -> None:
        """Add a row of data to the table."""
        table.add_row(
            str(row['id']),
            row['main_character'],
            row['alts'] if row['alts'] else 'None',  # Handle empty alt strings
            str(row['points_current'])
        )
