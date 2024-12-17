from typing import Dict, List, Tuple, Any
import xml.etree.ElementTree as ET
from utils.logger import get_logger
import logging

logger = get_logger(__name__)

class DataParser:
    """Handles parsing of XML data from EQDKP."""
    
    def parse_xml(self, file_path: str) -> Any:
        """
        Parse XML file with detailed error checking.
        
        Args:
            file_path: Path to the XML file
        
        Returns:
            Parsed data structure
        
        Raises:
            ValueError: If XML parsing fails
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            self._debug_xml_structure(root)
            self._validate_required_sections(root)
            
            return self._parse_data(root)
            
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format: {e}")
        except Exception as e:
            logging.exception("Error during XML parsing")
            raise ValueError(f"Error parsing XML: {e}")

    def _debug_xml_structure(self, root: ET.Element) -> None:
        """Log debug information about XML structure."""
        logging.debug(f"XML root tag: {root.tag}")
        logging.debug(f"Direct children of root: {[child.tag for child in root]}")
        
        if players := root.find('players'):
            logging.debug(f"Number of players found: {len(list(players))}")
            if first_player := players.find('player'):
                logging.debug(f"First player elements: {[elem.tag for elem in first_player]}")
            else:
                logging.warning("No player elements found")

    def _validate_required_sections(self, root: ET.Element) -> None:
        """Validate presence of required XML sections."""
        for section in ['eqdkp', 'players']:
            if root.find(section) is None:
                raise ValueError(f"Missing required '{section}' section")

    def _parse_data(self, root: ET.Element) -> Any:
        """
        Internal method to parse the XML data structure.
        Add logging before any .text access to identify which element is None.
        """
        # Add your existing parsing logic here with debug statements
        pass

    def _process_main_characters(self, players: ET.Element) -> Dict[str, Any]:
        """Process and extract main character data from XML."""
        main_character_data = {}
        
        for player in players.findall("player"):
            main_name = player.find("main_name").text
            name = player.find("name").text
            
            if main_name == name:  # This is a main character
                char_id = int(player.find("id").text)
                points = self._extract_points(player)
                
                main_character_data[main_name] = {
                    "id": char_id,
                    "points": points,
                    "alts": []
                }
                logger.info(f"Processed main character: {main_name} (ID: {char_id})")
                
        return main_character_data

    def _process_alt_characters(self, players: ET.Element, main_character_data: Dict[str, Any]) -> None:
        """Process and associate alt characters with their mains."""
        for player in players.findall("player"):
            main_name = player.find("main_name").text
            char_id = int(player.find("id").text)
            name = player.find("name").text

            if main_name in main_character_data and main_name != name:
                main_character_data[main_name]["alts"].append((char_id, name))
                logger.info(f"Alt '{name}' (ID: {char_id}) associated with main '{main_name}'")
            elif main_name not in main_character_data:
                logger.warning(f"Main character '{main_name}' not found for alt '{name}' (ID: {char_id})")

    @staticmethod
    def _extract_points(player: ET.Element) -> Dict[str, float]:
        """Extract point information from a player element."""
        return {
            "earned": float(player.find("points_earned").text),
            "spent": float(player.find("points_spent").text),
            "adjusted": float(player.find("points_adjusted").text),
            "current": float(player.find("points_current").text)
        }
