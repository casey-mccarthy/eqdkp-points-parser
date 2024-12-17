from typing import Dict, List, Tuple, Any
import xml.etree.ElementTree as ET
from utils.logger import get_logger
import logging
import json

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
            with open(file_path, 'r') as f:
                content = f.read()
                logger.debug(f"XML Content (first 500 chars): {content[:500]}")
        except Exception as e:
            logger.error(f"Error reading file: {e}")
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            self._debug_xml_structure(root)
            self._validate_required_sections(root)
            
            parsed_data = self._parse_data(root)
            
            # Save parsed data to debug file
            debug_file = 'debug_parsed_data.json'
            try:
                with open(debug_file, 'w') as f:
                    json.dump(parsed_data, f, indent=2)
                logger.info(f"Debug data saved to {debug_file}")
            except Exception as e:
                logger.error(f"Failed to save debug data: {e}")
            
            return parsed_data
            
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

    def _parse_data(self, root: ET.Element) -> Dict[str, Any]:
        """
        Internal method to parse the XML data structure.
        
        Args:
            root: Root element of the XML tree
            
        Returns:
            Dict containing parsed player data
            
        Raises:
            ValueError: If required elements are missing or malformed
        """
        try:
            players_element = root.find('players')
            if players_element is None:
                raise ValueError("No 'players' section found in XML")

            # First pass: Process main characters
            main_character_data = self._process_main_characters(players_element)
            
            # Second pass: Process alt characters
            self._process_alt_characters(players_element, main_character_data)
            
            return main_character_data
            
        except AttributeError as e:
            logger.error(f"XML structure error: {e}")
            raise ValueError(f"Malformed XML structure: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during data parsing: {e}")
            raise ValueError(f"Data parsing error: {e}")

    def _process_main_characters(self, players: ET.Element) -> Dict[str, Any]:
        """Process and extract main character data from XML."""
        main_character_data = {}
        
        for player in players.findall("player"):
            # Add debug logging for XML structure
            logger.debug(f"Processing player XML: {ET.tostring(player, encoding='unicode')}")
            
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

    def _extract_points(self, player: ET.Element) -> Dict[str, float]:
        """
        Extract points data from a player XML element with safe fallbacks.
        
        Args:
            player: XML element containing player data
            
        Returns:
            Dictionary containing earned and spent points, defaults to 0.0 if missing
        """
        try:
            points_earned = player.find("points_earned")
            points_spent = player.find("points_spent")
            
            # Use 0.0 as default value if points data is missing
            earned = float(points_earned.text) if points_earned is not None else 0.0
            spent = float(points_spent.text) if points_spent is not None else 0.0
            
            logger.warning(f"Missing points data for player {player.find('name').text}, using defaults") if points_earned is None or points_spent is None else None
            
            return {
                "earned": earned,
                "spent": spent
            }
        except (AttributeError, ValueError) as e:
            # Log the specific player data for debugging
            player_name = player.find('name').text if player.find('name') is not None else 'Unknown'
            logger.warning(f"Failed to extract points for player {player_name}, using defaults")
            return {
                "earned": 0.0,
                "spent": 0.0
            }
