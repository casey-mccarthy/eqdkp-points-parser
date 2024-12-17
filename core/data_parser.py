from typing import Dict, List, Tuple, Any
import xml.etree.ElementTree as ET
from utils.logger import get_logger

logger = get_logger(__name__)

class DataParser:
    """Handles parsing of XML data from EQDKP."""
    
    def parse_xml(self, xml_file: str) -> Dict[str, Any]:
        """
        Parse the XML file containing DKP data.
        
        Args:
            xml_file: Path to the XML file to parse
            
        Returns:
            Dict containing parsed character data
        """
        logger.info(f"Parsing XML file: {xml_file}")
        tree = ET.parse(xml_file)
        root = tree.getroot()
        players = root.find("players")
        
        # First pass: Process main characters
        main_character_data = self._process_main_characters(players)
        
        # Second pass: Process alts
        self._process_alt_characters(players, main_character_data)
        
        return self._prepare_final_data(main_character_data)

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
