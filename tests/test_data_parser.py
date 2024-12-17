import unittest
from core.data_parser import DataParser
from typing import Dict, Any
import os

class TestDataParser(unittest.TestCase):
    """Test case for the DataParser class."""

    def setUp(self) -> None:
        """Set up the test case with the DataParser instance."""
        self.parser = DataParser()
        # Adjust the file path to point to the correct location in the tests folder
        self.file_path = os.path.join(os.path.dirname(__file__), 'sample_data.xml')

    def test_parse_xml_file(self) -> None:
        """Test parsing of XML data from a file for the character Dainae."""
        # Parse the XML file
        result: Dict[str, Any] = self.parser.parse_xml(self.file_path)

        # Define expected output for the character Dainae
        expected_dainae = {
            'id': 56,
            'class_name': 'Enchanter',
            'active': True,
            'points': {
                'current': 297.0,
                'earned': 3315.0,
                'spent': 3553.0,
                'current_with_twink': 297.0,
                'earned_with_twink': 3315.0,
                'spent_with_twink': 3553.0
            },
            'alts': [
                {
                    'id': 58,
                    'name': 'Berik',
                    'class_name': 'Paladin',
                    'points': {
                        'current': -302.0,
                        'earned': 681.0,
                        'spent': 1005.0
                    }
                },
                {
                    'id': 57,
                    'name': 'Byee',
                    'class_name': 'Monk',
                    'points': {
                        'current': -229.0,
                        'earned': 1154.0,
                        'spent': 1383.0
                    }
                },
                {
                    'id': 2381,
                    'name': 'Cneasaigh',
                    'class_name': 'Cleric',
                    'points': {
                        'current': 155.0,
                        'earned': 131.0,
                        'spent': 0.0
                    }
                },
                {
                    'id': 4420,
                    'name': 'Codlatach',
                    'class_name': 'Shaman',
                    'points': {
                        'current': 3.0,
                        'earned': 3.0,
                        'spent': 0.0
                    }
                },
                {
                    'id': 2398,
                    'name': 'Nokio',
                    'class_name': 'Bard',
                    'points': {
                        'current': 33.0,
                        'earned': 33.0,
                        'spent': 0.0
                    }
                },
                {
                    'id': 2382,
                    'name': 'Paebst',
                    'class_name': 'Druid',
                    'points': {
                        'current': 0.0,
                        'earned': 0.0,
                        'spent': 0.0
                    }
                }
            ]
        }

        # Check if the character 'Dainae' is in the result
        self.assertIn('Dainae', result)

        # Assert the result for Dainae matches the expected output
        self.assertEqual(result['Dainae'], expected_dainae)

    def test_xml_structure(self) -> None:
        """Test if the XML file has the correct structure."""
        # Parse the XML file
        result: Dict[str, Any] = self.parser.parse_xml(self.file_path)

        # Check if the main character 'Forpor' is in the result
        self.assertIn('Forpor', result)

        # Check if 'Forpor' has the expected keys
        self.assertIn('id', result['Forpor'])
        self.assertIn('class_name', result['Forpor'])
        self.assertIn('active', result['Forpor'])
        self.assertIn('points', result['Forpor'])
        self.assertIn('alts', result['Forpor'])

    def test_parse_dainae(self) -> None:
        """Test parsing of XML data for the character Dainae."""
        # Parse the XML file
        result: Dict[str, Any] = self.parser.parse_xml(self.file_path)

        # Check if the character 'Dainae' is in the result
        self.assertIn('Dainae', result)

        # Check if 'Dainae' has the expected keys
        self.assertIn('id', result['Dainae'])
        self.assertIn('class_name', result['Dainae'])
        self.assertIn('active', result['Dainae'])
        self.assertIn('points', result['Dainae'])
        self.assertIn('alts', result['Dainae'])

if __name__ == '__main__':
    unittest.main() 