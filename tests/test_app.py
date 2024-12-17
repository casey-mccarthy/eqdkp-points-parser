import unittest
from unittest.mock import Mock, patch
import pandas as pd
from app.main import EQDKPParserApp
from interface.cli import CLI
from utils.progress import ProgressManager

class TestEQDKPParserApp(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = EQDKPParserApp()
        
    @patch('app.main.AppConfig')
    def test_validate_config_with_api_key(self, mock_config):
        """Test config validation with valid API key."""
        mock_config.load().api_key = "test_key"
        self.app.config = mock_config.load()
        
        # Should not raise an exception
        self.app._validate_config()
        
    @patch('app.main.AppConfig')
    def test_validate_config_without_api_key(self, mock_config):
        """Test config validation without API key."""
        mock_config.load().api_key = None
        self.app.config = mock_config.load()
        
        with self.assertRaises(ValueError):
            self.app._validate_config()
            
    @patch('app.main.DataFetcher')
    def test_fetch_and_process_data_success(self, mock_fetcher):
        """Test successful data fetching and processing."""
        mock_fetcher.return_value.fetch_data.return_value = "test.xml"
        self.app.data_fetcher = mock_fetcher.return_value
        
        # Mock the data processing chain
        self.app.data_parser.parse_xml = Mock(return_value={"data": "test"})
        self.app.data_processor.process_data = Mock(
            return_value=pd.DataFrame({'test': [1, 2, 3]})
        )
        
        result = self.app._fetch_and_process_data()
        self.assertIsInstance(result, pd.DataFrame)
        
    @patch('app.main.DataFetcher')
    def test_fetch_and_process_data_failure(self, mock_fetcher):
        """Test failed data fetching."""
        mock_fetcher.return_value.fetch_data.return_value = None
        self.app.data_fetcher = mock_fetcher.return_value
        
        with self.assertRaises(RuntimeError):
            self.app._fetch_and_process_data()

class TestCLI(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_data = pd.DataFrame({
            'id': [1, 2],
            'main_character': ['Test1', 'Test2'],
            'alts': ['Alt1, Alt2', None],
            'points_current': [100, 200]
        })
        self.cli = CLI(self.sample_data)
        
    def test_handle_character_search_found(self):
        """Test character search with existing character."""
        with patch('interface.display.DisplayManager.display_data') as mock_display:
            self.cli._handle_character_search(['Test1'])
            mock_display.assert_called_once()
            
    def test_handle_top_display(self):
        """Test top N characters display."""
        with patch('interface.display.DisplayManager.display_data') as mock_display:
            self.cli._handle_top_display(['2'])
            mock_display.assert_called_once()
            
    def test_handle_exit(self):
        """Test exit command by verifying it raises SystemExit."""
        with self.assertRaises(SystemExit) as cm:
            self.cli._handle_exit([])
        self.assertEqual(cm.exception.code, 0)

class TestProgressManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.progress = ProgressManager()
        
    @patch('rich.console.Console.print')
    def test_show_progress_success(self, mock_print):
        """Test progress display with success message."""
        self.progress.show_progress("Test message", success=True)
        mock_print.assert_called_once()
        
    @patch('rich.console.Console.print')
    def test_show_progress_info(self, mock_print):
        """Test progress display with info message."""
        self.progress.show_progress("Test message", success=False)
        mock_print.assert_called_once()

if __name__ == '__main__':
    unittest.main()