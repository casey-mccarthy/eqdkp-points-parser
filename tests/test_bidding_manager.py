import unittest
from unittest.mock import patch
import pandas as pd
from core.bidding_manager import BiddingManager

class TestBiddingManager(unittest.TestCase):
    """Test suite for the BiddingManager class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.character_data = pd.DataFrame({
            'main_character': ['Test1', 'Test2', 'Test3'],
            'points_current': [100, 200, 150]
        })
        self.bidding_manager = BiddingManager(self.character_data)

    def test_add_character(self) -> None:
        """Test adding a character to the bid."""
        self.bidding_manager.start_bid()
        self.bidding_manager.add_character('Test1')
        self.assertEqual(len(self.bidding_manager.current_bid), 1)
        self.assertEqual(self.bidding_manager.current_bid[0]['main_character'], 'Test1')

    def test_add_duplicate_character(self) -> None:
        """Test adding a duplicate character to the bid."""
        self.bidding_manager.start_bid()
        self.bidding_manager.add_character('Test1')
        self.bidding_manager.add_character('Test1')  # Attempt to add duplicate
        self.assertEqual(len(self.bidding_manager.current_bid), 1)  # Should still be 1

    def test_display_sorted_bid(self) -> None:
        """Test sorting of characters in the bid."""
        self.bidding_manager.start_bid()
        self.bidding_manager.add_character('Test1')
        self.bidding_manager.add_character('Test2')
        self.bidding_manager.add_character('Test3')
        sorted_names = [char['main_character'] for char in self.bidding_manager.current_bid]
        self.assertEqual(sorted_names, ['Test2', 'Test3', 'Test1'])  # Sorted by points

    def test_end_bid(self) -> None:
        """Test ending the bid session."""
        self.bidding_manager.start_bid()
        self.bidding_manager.add_character('Test1')
        self.bidding_manager.end_bid()
        self.assertEqual(len(self.bidding_manager.current_bid), 0)  # Bid should be cleared

if __name__ == '__main__':
    unittest.main() 