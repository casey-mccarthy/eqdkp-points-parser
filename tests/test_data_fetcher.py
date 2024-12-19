import unittest
from unittest.mock import Mock, patch
import requests
from core.data_fetcher import DataFetcher

class TestDataFetcher(unittest.TestCase):
    """Test suite for DataFetcher class."""

    def setUp(self):
        """Set up test fixtures."""
        self.fetcher = DataFetcher()
        self.api_token = "test_token"

    @patch('requests.get')
    def test_fetch_character_data_success(self, mock_get):
        """Test successful character data fetching."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<xml>test data</xml>"
        mock_get.return_value = mock_response

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            result = self.fetcher.fetch_character_data(self.api_token)
            self.assertIsNotNone(result)
            mock_file.assert_called_once()

    @patch('requests.get')
    def test_fetch_character_data_api_error(self, mock_get):
        """Test handling of API error response for character data."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.fetcher.fetch_character_data(self.api_token)
        self.assertIsNone(result)

    @patch('requests.get')
    def test_fetch_character_data_network_error(self, mock_get):
        """Test handling of network error for character data."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        result = self.fetcher.fetch_character_data(self.api_token)
        self.assertIsNone(result)

    @patch('requests.get')
    def test_fetch_ranks_data_success(self, mock_get):
        """Test successful ranks data fetching."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<xml>test data</xml>"
        mock_get.return_value = mock_response

        result = self.fetcher.fetch_ranks_data(self.api_token)
        self.assertIsNotNone(result)

    @patch('requests.get')
    def test_fetch_ranks_data_api_error(self, mock_get):
        """Test handling of API error response for ranks data."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.fetcher.fetch_ranks_data(self.api_token)
        self.assertIsNone(result)

    @patch('requests.get')
    def test_fetch_ranks_data_network_error(self, mock_get):
        """Test handling of network error for ranks data."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        result = self.fetcher.fetch_ranks_data(self.api_token)
        self.assertIsNone(result) 