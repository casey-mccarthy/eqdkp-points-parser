# tests/test_api_refs.py

import unittest
from unittest.mock import patch, Mock
import requests
from core.api_refs import (
    APIReadPaths, call_api, get_user_chars, get_calendar_events_list,
    get_calendar_event_details, get_points, get_data, search_user,
    search_character, get_me
)

class TestAPIReadPaths(unittest.TestCase):
    """Test suite for APIReadPaths class and related functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.api_token = "dummy_token"
        self.base_url = "https://dkp.kwsm.app"

    def test_build_url(self):
        """Test URL building with parameters."""
        path = APIReadPaths.USER_CHARS
        url = APIReadPaths.build_url(path, api_token=self.api_token)
        expected = f"{self.base_url}/api.php?function=user_chars&atoken={self.api_token}&atype=api"
        self.assertEqual(url, expected)

    @patch('core.api_refs.requests.get')
    def test_call_api_get_success(self, mock_get):
        """Test successful GET API call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response

        result = call_api("http://test.com", method="GET")
        self.assertEqual(result, {"data": "test"})

    @patch('core.api_refs.requests.post')
    def test_call_api_post_success(self, mock_post):
        """Test successful POST API call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = {"data": "test"}
        mock_post.return_value = mock_response

        result = call_api("http://test.com", method="POST", payload={"test": "data"})
        self.assertEqual(result, {"data": "test"})

    def test_call_api_invalid_method(self):
        """Test API call with invalid HTTP method."""
        with self.assertRaises(ValueError):
            call_api("http://test.com", method="PUT")

    @patch('core.api_refs.requests.get')
    def test_call_api_request_exception(self, mock_get):
        """Test API call with request exception."""
        mock_get.side_effect = requests.exceptions.RequestException("Test error")
        with self.assertRaises(Exception) as context:
            call_api("http://test.com")
        self.assertIn("API call to http://test.com failed", str(context.exception))

    @patch('core.api_refs.requests.get')
    def test_get_data(self, mock_get):
        """Test get_data function."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response

        result = get_data(self.api_token)
        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with(
            f"{self.base_url}/api.php?function=data&atoken={self.api_token}&atype=api",
            headers=None
        )

    @patch('core.api_refs.requests.get')
    def test_get_points_with_filters(self, mock_get):
        """Test get_points function with filters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = {"points": "test"}
        mock_get.return_value = mock_response

        result = get_points(self.api_token, filter_type="class", filter_id=1)
        self.assertEqual(result, {"points": "test"})
        expected_url = f"{self.base_url}/api.php?function=points&atoken={self.api_token}&atype=api&filter=class&filterid=1"
        mock_get.assert_called_once_with(expected_url, headers=None)

    @patch('core.api_refs.requests.get')
    def test_non_json_response(self, mock_get):
        """Test handling of non-JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'text/plain'}
        mock_response.text = "Plain text response"
        mock_get.return_value = mock_response

        result = call_api("http://test.com")
        self.assertEqual(result, "Plain text response")

    @patch('core.api_refs.requests.get')
    def test_get_calendar_events_list_with_params(self, mock_get):
        """Test calendar events list with custom parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = {"events": ["event1", "event2"]}
        mock_get.return_value = mock_response

        result = get_calendar_events_list(self.api_token, raids_only=0, number=5)
        self.assertEqual(result, {"events": ["event1", "event2"]})
        expected_url = (f"{self.base_url}/api.php?function=calevents_list&atoken={self.api_token}"
                       f"&atype=api&raids_only=0&number=5")
        mock_get.assert_called_once_with(expected_url, headers=None)

if __name__ == "__main__":
    unittest.main()
