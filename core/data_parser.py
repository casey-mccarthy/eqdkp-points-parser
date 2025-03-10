import xml.etree.ElementTree as ET
from utils.logger import get_logger
from core.database import DatabaseManager
from core.models import Character

logger = get_logger(__name__)


class DataParser:
    """Handles parsing of XML data from EQDKP with focus on character relationships."""
    
    def __init__(self) -> None:
        """Initialize the DataParser with a DatabaseManager instance."""
        self.db_manager = DatabaseManager()
    
    def parse_character_data(self, xml_data: str) -> None:
        """Parse the XML data and save to the database."""
        session = self.db_manager.get_session()
        logger.info("Starting XML data parsing")
        
        try:    
            root = ET.fromstring(xml_data)
            logger.info("Successfully parsed XML string into ElementTree")

            players_element = root.find('players')
            if players_element is None:
                logger.error("No players element found in XML data")
                return
            
            for player in players_element.findall('player'):
                player_name = player.findtext('name', 'Unknown')
                logger.debug(f"Processing player: {player_name}")
                
                character_model = Character(
                    id=int(player.findtext('id', 0)),
                    name=player_name,
                    class_id=int(player.findtext('class_id', 0)),
                    class_name=player.findtext('class_name', 'Unknown'),
                    active=bool(int(player.findtext('active', 0))),
                    hidden=bool(int(player.findtext('hidden', 0))),
                    main_id=int(player.findtext('main_id', 0)) if player.find('main_id') is not None else None,
                    main_name=player.findtext('main_name', None),
                    rank_id=None,
                    rank_name=None,
                    current=float(player.findtext('points/multidkp_points/points_current', 0)),
                    current_with_twink=float(player.findtext('points/multidkp_points/points_current_with_twink', 0)),
                    earned=float(player.findtext('points/multidkp_points/points_earned', 0)),
                    earned_with_twink=float(player.findtext('points/multidkp_points/points_earned_with_twink', 0)),
                    spent=float(player.findtext('points/multidkp_points/points_spent', 0)),
                    spent_with_twink=float(player.findtext('points/multidkp_points/points_spent_with_twink', 0)),
                    adjustment=float(player.findtext('points/multidkp_points/points_adjustment', 0)),
                    adjustment_with_twink=float(player.findtext('points/multidkp_points/points_adjustment_with_twink', 0))
                )
                
                session.merge(character_model)
            
            session.commit()
            logger.info("XML parsing complete.")
        
        except Exception as e:
            logger.error(f"Critical error parsing XML data: {e}")
            session.rollback()
            raise
        
        finally:
            session.close()
            logger.info("Database session closed")
    
    def parse_character_rank_data(self, xml_data: str) -> None:
        """
        Parse the XML data from the character_rank API call and update character ranks.

        Args:
            xml_data (str): The XML data as a string.
        """
        session = self.db_manager.get_session()
        logger.info("Starting XML data parsing")
        
        try:
            root = ET.fromstring(xml_data)
            logger.info("Successfully parsed XML string into ElementTree")

            # Navigate to the characters element
            characters_element = root.find('characters')
            if characters_element is None:
                logger.error("No characters element found in XML data")
                return

            for character in characters_element:
                character_name = character.findtext('character_name', 'Unknown')
                character_id = int(character.findtext('character_id', 0))
                rank_id = int(character.findtext('rank_id', 0))
                rank_name = character.findtext('rank_name', 'Unknown')

                # Retrieve the character from the database
                character_data = session.query(Character).filter_by(id=character_id).first()
                
                if character_data is not None:
                    logger.debug(f"Updating rank for character ID {character_id}")
                    character_data.rank_id = rank_id
                    character_data.rank_name = rank_name
                else:
                    logger.warning(f"Character {character_name} with ID {character_id} not found in the database")

            session.commit()
            logger.info("Character ranks updated successfully")

        except Exception as e:
            logger.error(f"Error parsing XML data: {e}")
            logger.exception("Full traceback:")
            session.rollback()
            raise  # Re-raise the exception after logging

        finally:
            session.close()
            logger.info("Database session closed")
