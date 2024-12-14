# tests/test_api_refs.py

import unittest
from unittest.mock import patch
from api_refs import get_user_chars, get_calendar_events_list, get_calendar_event_details, get_points, search_user, search_character, get_me

class TestAPIReadPaths(unittest.TestCase):

    @patch('api_refs.requests.get')
    def test_get_user_chars(self, mock_get):
        # Mock the response for the GET request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"characters": ["Character1", "Character2"]}
        
        response = get_user_chars(api_token="dummy_token")
        self.assertEqual(response, {"characters": ["Character1", "Character2"]})
        mock_get.assert_called_once_with(
            "https://dkp.kwsm.app/api.php?function=user_chars&atoken=dummy_token&atype=api",
            headers=None
        )

    @patch('api_refs.requests.get')
    def test_get_calendar_events_list(self, mock_get):
        # Mock the response for the GET request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"events": ["Event1", "Event2"]}
        
        response = get_calendar_events_list(api_token="dummy_token", raids_only=0, number=5)
        self.assertEqual(response, {"events": ["Event1", "Event2"]})
        mock_get.assert_called_once_with(
            "https://dkp.kwsm.app/api.php?function=calevents_list&atoken=dummy_token&atype=api&raids_only=0&number=5",
            headers=None
        )

    @patch('api_refs.requests.get')
    def test_get_calendar_event_details(self, mock_get):
        # Mock the response for the GET request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"event": {"id": 1, "name": "Event1"}}
        
        response = get_calendar_event_details(api_token="dummy_token", event_id=1)
        self.assertEqual(response, {"event": {"id": 1, "name": "Event1"}})
        mock_get.assert_called_once_with(
            "https://dkp.kwsm.app/api.php?function=calevents_details&eventid=1&atoken=dummy_token&atype=api",
            headers=None
        )

    @patch('api_refs.requests.get')
    def test_get_points(self, mock_get):
        # Mock the response for the GET request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"points": 100}
        
        response = get_points(api_token="dummy_token", filter_type="class", filter_id=2)
        self.assertEqual(response, {"points": 100})
        mock_get.assert_called_once_with(
            "https://dkp.kwsm.app/api.php?function=points&atoken=dummy_token&atype=api&filter=class&filterid=2",
            headers=None
        )

    @patch('api_refs.requests.get')
    def test_search_user(self, mock_get):
        # Mock the response for the GET request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"user": "User1"}
        
        response = search_user(api_token="dummy_token", username="User1")
        self.assertEqual(response, {"user": "User1"})
        mock_get.assert_called_once_with(
            "https://dkp.kwsm.app/api.php?function=search&in=username&for=User1&atoken=dummy_token&atype=api",
            headers=None
        )

    @patch('api_refs.requests.get')
    def test_search_character(self, mock_get):
        # Mock the response for the GET request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"character": "Character1"}
        
        response = search_character(api_token="dummy_token", charname="Character1")
        self.assertEqual(response, {"character": "Character1"})
        mock_get.assert_called_once_with(
            "https://dkp.kwsm.app/api.php?function=search&in=charname&for=Character1&atoken=dummy_token&atype=api",
            headers=None
        )

    @patch('api_refs.requests.get')
    def test_get_me(self, mock_get):
        # Mock the response for the GET request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"user": "AuthenticatedUser"}
        
        response = get_me(api_token="dummy_token")
        self.assertEqual(response, {"user": "AuthenticatedUser"})
        mock_get.assert_called_once_with(
            "https://dkp.kwsm.app/api.php?function=me&atoken=dummy_token&atype=api",
            headers=None
        )

if __name__ == "__main__":
    unittest.main()
