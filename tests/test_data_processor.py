import unittest
from unittest.mock import Mock, patch
import pandas as pd
from core.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    """Test suite for DataProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = DataProcessor()
        self.sample_data = {
            'Character1': {
                'id': 1,
                'class_name': 'Warrior',
                'points': {
                    'current_with_twink': 100,
                    'earned_with_twink': 150,
                    'spent_with_twink': 50
                },
                'alts': [
                    {'name': 'Alt1', 'id': 2},
                    {'name': 'Alt2', 'id': 3}
                ]
            }
        }

    def test_process_data_success(self):
        """Test successful data processing with valid input."""
        result = self.processor.process_data(self.sample_data)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['main_character'], 'Character1')
        self.assertEqual(result.iloc[0]['points_current'], 100)
        self.assertEqual(result.iloc[0]['alts'], 'Alt1, Alt2')

    def test_process_data_empty_input(self):
        """Test processing with empty input data."""
        result = self.processor.process_data({})
        self.assertTrue(result.empty)

    def test_process_data_with_no_alts(self):
        """Test processing character data without alts."""
        data = {
            'Character1': {
                'id': 1,
                'class_name': 'Warrior',
                'points': {
                    'current_with_twink': 100,
                    'earned_with_twink': 150,
                    'spent_with_twink': 50
                },
                'alts': []
            }
        }
        result = self.processor.process_data(data)
        self.assertEqual(result.iloc[0]['alts'], '')

    def test_process_data_save_to_file(self):
        """Test saving processed data to CSV file."""
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            self.processor.process_data(self.sample_data, 'test.csv')
            mock_to_csv.assert_called_once_with('test.csv', index=False)

    def test_process_data_invalid_input(self):
        """Test processing with invalid input structure."""
        invalid_data = {'invalid': 'structure'}
        with self.assertRaises(Exception):
            self.processor.process_data(invalid_data) 