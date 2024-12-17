from typing import Dict, List, Any
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from utils.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

@dataclass
class CharacterPoints:
    """Data class to store character point information."""
    current: float
    earned: float
    spent: float
    current_with_twink: float
    earned_with_twink: float
    spent_with_twink: float
    adjustment: float
    adjustment_with_twink: float

@dataclass
class Character:
    """Data class to store character information."""
    id: int
    name: str
    class_id: int
    class_name: str
    active: bool
    points: CharacterPoints
    main_id: int
    main_name: str

class DataParser:
    """Handles parsing of XML data from EQDKP with focus on character relationships."""
    
    def parse_xml(self, file_path: str) -> Dict[str, Any]:
        """
        Parse XML file and organize characters by main/alt relationships.
        
        Args:
            file_path: Path to the XML file
        
        Returns:
            Dict containing organized character data
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # First pass: collect all characters
            characters: Dict[str, Character] = {}
            main_characters: Dict[str, Dict[str, Any]] = {}
            
            players = root.find('players')
            if not players:
                raise ValueError("No players section found in XML")
                
            # Process all characters
            for player in players.findall('player'):
                char = self._parse_character(player)
                characters[char.name] = char
                
                # If character is their own main, add to main_characters
                if char.name == char.main_name:
                    main_characters[char.name] = {
                        'character': char,
                        'alts': []
                    }
            
            # Second pass: associate alts with mains
            for char in characters.values():
                if char.name != char.main_name and char.main_name in main_characters:
                    main_characters[char.main_name]['alts'].append(char)
            
            return self._format_output(main_characters)
            
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {e}")
            raise ValueError(f"Invalid XML format: {e}")
        except Exception as e:
            logger.error(f"Error during parsing: {e}")
            raise ValueError(f"Error parsing data: {e}")

    def _parse_character(self, player: ET.Element) -> Character:
        """Parse individual character data from XML element."""
        points_elem = player.find('points/multidkp_points')
        
        points = CharacterPoints(
            current=float(points_elem.find('points_current').text),
            earned=float(points_elem.find('points_earned').text),
            spent=float(points_elem.find('points_spent').text),
            current_with_twink=float(points_elem.find('points_current_with_twink').text),
            earned_with_twink=float(points_elem.find('points_earned_with_twink').text),
            spent_with_twink=float(points_elem.find('points_spent_with_twink').text),
            adjustment=float(points_elem.find('points_adjustment').text),
            adjustment_with_twink=float(points_elem.find('points_adjustment_with_twink').text)
        )
        
        return Character(
            id=int(player.find('id').text),
            name=player.find('name').text,
            class_id=int(player.find('class_id').text),
            class_name=player.find('class_name').text,
            active=bool(int(player.find('active').text)),
            points=points,
            main_id=int(player.find('main_id').text),
            main_name=player.find('main_name').text
        )

    def _format_output(self, main_characters: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Format the parsed data into the final output structure."""
        output = {}
        
        for main_name, data in main_characters.items():
            main_char = data['character']
            output[main_name] = {
                'id': main_char.id,
                'class_name': main_char.class_name,
                'active': main_char.active,
                'points': {
                    'current': main_char.points.current,
                    'earned': main_char.points.earned,
                    'spent': main_char.points.spent,
                    'current_with_twink': main_char.points.current_with_twink,
                    'earned_with_twink': main_char.points.earned_with_twink,
                    'spent_with_twink': main_char.points.spent_with_twink
                },
                'alts': [{
                    'id': alt.id,
                    'name': alt.name,
                    'class_name': alt.class_name,
                    'points': {
                        'current': alt.points.current,
                        'earned': alt.points.earned,
                        'spent': alt.points.spent
                    }
                } for alt in data['alts']]
            }
        
        return output
