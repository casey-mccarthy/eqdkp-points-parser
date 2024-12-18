from typing import Dict, List, Any
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from utils.logger import get_logger
import pandas as pd
from core.database import DatabaseManager
from core.models import Character, CharacterPoints

logger = get_logger(__name__)


class DataParser:
    """Handles parsing of XML data from EQDKP with focus on character relationships."""
    
    def __init__(self) -> None:
        """Initialize the DataParser with a DatabaseManager instance."""
        self.db_manager = DatabaseManager()
    
    def parse_data(self, xml_data: str) -> None:
        """Parse the XML data and save to the database.
        
        Args:
            xml_data (str): XML string containing character and DKP data
        """
        session = self.db_manager.get_session()
        logger.info("Starting XML data parsing")
        
        try:    
            root = ET.fromstring(xml_data)
            logger.info("Successfully parsed XML string into ElementTree")

            # Get the players element which contains all player nodes
            players_element = root.find('players')
            if players_element is None:
                logger.error("No players element found in XML data")
                return
            
            total_players = len(players_element)
            logger.info(f"Found {total_players} player records to process")
            
            processed_count = 0
            error_count = 0
            
            for player in players_element.findall('player'):
                try:
                    player_name = player.findtext('name', 'Unknown')
                    logger.info(f"Processing player: {player_name}")
                    
                    # Extract character data with safe defaults
                    character_model = Character(
                        id=int(player.findtext('id', 0)),
                        name=player_name,
                        class_id=int(player.findtext('class_id', 0)),
                        class_name=player.findtext('class_name', 'Unknown'),
                        active=bool(int(player.findtext('active', 0))),
                        hidden=bool(int(player.findtext('hidden', 0))),
                        main_id=int(player.findtext('main_id', 0)) if player.find('main_id') is not None else None,
                        main_name=player.findtext('main_name', None)
                    )
                    
                    logger.info(f"Created character model for {player_name} (ID: {character_model.id})")
                    
                    # Extract points data
                    points_element = player.find('points/multidkp_points')
                    if points_element is not None:
                        logger.info(f"Processing DKP points for {player_name}")
                        points_model = CharacterPoints(
                            character_id=character_model.id,
                            current=float(points_element.findtext('points_current', 0)),
                            current_with_twink=float(points_element.findtext('points_current_with_twink', 0)),
                            earned=float(points_element.findtext('points_earned', 0)),
                            earned_with_twink=float(points_element.findtext('points_earned_with_twink', 0)),
                            spent=float(points_element.findtext('points_spent', 0)),
                            spent_with_twink=float(points_element.findtext('points_spent_with_twink', 0)),
                            adjustment=float(points_element.findtext('points_adjustment', 0)),
                            adjustment_with_twink=float(points_element.findtext('points_adjustment_with_twink', 0))
                        )
                        
                        # Link points to character
                        character_model.points = points_model
                        logger.info(f"DKP points processed for {player_name}: current={points_model.current}, earned={points_model.earned}")
                    else:
                        logger.warning(f"No DKP points data found for {player_name}")
                    
                    # Add to session and commit
                    session.merge(character_model)
                    processed_count += 1
                    
                    if processed_count % 100 == 0:  # Log progress every 100 players
                        logger.info(f"Processed {processed_count}/{total_players} players")
                    
                except Exception as player_error:
                    error_count += 1
                    logger.error(f"Error processing player {player_name}: {player_error}")
                    logger.exception("Player processing traceback:")
                    continue  # Continue with next player
                
            session.commit()
            logger.info(f"XML parsing complete. Successfully processed {processed_count} players with {error_count} errors")
            
            # Log summary statistics
            if error_count > 0:
                logger.warning(f"Encountered {error_count} errors while processing {total_players} players")
            else:
                logger.info("All players processed successfully")

        except Exception as e:
            logger.error(f"Critical error parsing XML data: {e}")
            logger.exception("Full traceback:")
            session.rollback()
            raise  # Re-raise the exception after logging
        
        finally:
            session.close()
            logger.info("Database session closed")
    
