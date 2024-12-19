import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base, Character
from core.data_parser import DataParser

class TestDataParser(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create an in-memory SQLite database
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Initialize the DataParser with a mock DatabaseManager
        self.data_parser = DataParser()
        self.data_parser.db_manager.Session = self.Session

        # Add test data to the database
        self._add_test_data()

    def _add_test_data(self):
        """Add test data to the database."""
        character = Character(
            id=56,
            name='Dainae',
            class_id=1,
            class_name='Enchanter',
            active=True,
            current=297.0,
            earned=3315.0,
            spent=3553.0,
            current_with_twink=297.0,
            earned_with_twink=3315.0,
            spent_with_twink=3553.0
        )
        self.session.add(character)
        self.session.commit()

    def tearDown(self):
        """Clean up after each test method."""
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_parse_character_data(self):
        """Test parsing of character data."""
        # Simulate parsing XML data
        xml_data = """<players>
                        <player>
                            <id>56</id>
                            <name>Dainae</name>
                            <class_id>1</class_id>
                            <class_name>Enchanter</class_name>
                            <active>1</active>
                            <points>
                                <multidkp_points>
                                    <points_current>297.0</points_current>
                                    <points_earned>3315.0</points_earned>
                                    <points_spent>3553.0</points_spent>
                                </multidkp_points>
                            </points>
                        </player>
                      </players>"""
        self.data_parser.parse_character_data(xml_data)

        # Verify the character data in the database
        character = self.session.query(Character).filter_by(name='Dainae').first()
        self.assertIsNotNone(character)
        self.assertEqual(character.current, 297.0)
        self.assertEqual(character.earned, 3315.0)
        self.assertEqual(character.spent, 3553.0)

if __name__ == '__main__':
    unittest.main() 