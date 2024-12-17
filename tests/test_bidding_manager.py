import unittest
from unittest.mock import patch
import pandas as pd
from core.bidding_manager import BiddingManager

class TestBiddingManager(unittest.TestCase):
    """Test suite for the BiddingManager class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.character_data = pd.DataFrame({
            'id': [1, 2, 3],
            'main_character': ['Test1', 'Test2', 'Test3'],
            'alts': ['Alt1, Alt2', '', 'Alt3'],
            'points_current': [100, 200, 150]
        })
        self.bidding_manager = BiddingManager(self.character_data)

    @patch('rich.console.Console.print')
    def test_add_character(self, mock_print) -> None:
        """Test adding a character to the bid."""
        self.bidding_manager.start_bid()
        self.bidding_manager.add_character('Test1')
        self.assertEqual(len(self.bidding_manager.current_bid), 1)
        self.assertEqual(self.bidding_manager.current_bid[0]['main_character'], 'Test1')
        mock_print.assert_any_call("[cyan]Added Test1 to the bid.[/cyan]")

    @patch('rich.console.Console.print')
    def test_add_duplicate_character(self, mock_print) -> None:
        """Test adding a duplicate character to the bid."""
        self.bidding_manager.start_bid()
        self.bidding_manager.add_character('Test1')
        self.bidding_manager.add_character('Test1')  # Attempt to add duplicate
        self.assertEqual(len(self.bidding_manager.current_bid), 1)  # Should still be 1
        mock_print.assert_any_call("[yellow]Character 'Test1' is already in the bid![/yellow]")

    @patch('rich.console.Console.print')
    def test_display_sorted_bid(self, mock_print) -> None:
        """Test sorting of characters in the bid."""
        self.bidding_manager.start_bid()
        self.bidding_manager.add_character('Test1')
        self.bidding_manager.add_character('Test2')
        self.bidding_manager.add_character('Test3')
        sorted_names = [char['main_character'] for char in self.bidding_manager.current_bid]
        self.assertEqual(sorted_names, ['Test2', 'Test3', 'Test1'])  # Sorted by points
        mock_print.assert_any_call("[cyan]Added Test2 to the bid.[/cyan]")
        mock_print.assert_any_call("[cyan]Added Test3 to the bid.[/cyan]")

    @patch('rich.console.Console.print')
    def test_end_bid(self, mock_print) -> None:
        """Test ending the bid session."""
        self.bidding_manager.start_bid()
        self.bidding_manager.add_character('Test1')
        self.bidding_manager.end_bid()
        self.assertEqual(len(self.bidding_manager.current_bid), 0)  # Bid should be cleared
        mock_print.assert_any_call("[yellow]Bidding session ended![/yellow]")

if __name__ == '__main__':
    unittest.main() 