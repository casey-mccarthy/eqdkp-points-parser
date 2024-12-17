import unittest
from unittest.mock import patch
import pandas as pd
from interface.cli import CLI

class TestCLI(unittest.TestCase):
    """Test suite for the CLI class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.character_data = pd.DataFrame({
            'main_character': ['Test1', 'Test2', 'Test3'],
            'points_current': [100, 200, 150]
        })
        self.cli = CLI(self.character_data)

    # test to check if the user sorting works
    def test_user_sorting(self) -> None:
        self.cli.bidding_manager.start_bid()
        self.cli.bidding_manager.add_character('Test1')
        self.cli.bidding_manager.add_character('Test2')
        self.cli.bidding_manager.add_character('Test3')
        current_bid_names = [char['main_character'] for char in self.cli.bidding_manager.current_bid]
        self.assertEqual(current_bid_names, ['Test2', 'Test3', 'Test1'])

    # confirm that user can't add duplicate characters
    def test_duplicate_characters(self) -> None:
        self.cli.bidding_manager.start_bid()
        self.cli.bidding_manager.add_character('Test1')
        self.cli.bidding_manager.add_character('Test1')
        self.assertEqual(len(self.cli.bidding_manager.current_bid), 1)

if __name__ == '__main__':
    unittest.main() 