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
    def test_fetch_data_success(self, mock_get):
        """Test successful data fetching."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<xml>test data</xml>"
        mock_get.return_value = mock_response

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            result = self.fetcher.fetch_data(self.api_token)
            self.assertIsNotNone(result)
            mock_file.assert_called_once()

    @patch('requests.get')
    def test_fetch_data_api_error(self, mock_get):
        """Test handling of API error response."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.fetcher.fetch_data(self.api_token)
        self.assertIsNone(result)

    @patch('requests.get')
    def test_fetch_data_network_error(self, mock_get):
        """Test handling of network error."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        result = self.fetcher.fetch_data(self.api_token)
        self.assertIsNone(result)

    @patch('requests.get')
    def test_fetch_data_file_error(self, mock_get):
        """Test handling of file writing error."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<xml>test data</xml>"
        mock_get.return_value = mock_response

        with patch('builtins.open') as mock_file:
            mock_file.side_effect = IOError("File error")
            result = self.fetcher.fetch_data(self.api_token)
            self.assertIsNone(result) 