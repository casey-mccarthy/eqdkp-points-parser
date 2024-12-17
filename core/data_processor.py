from typing import Dict, List, Any
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

class DataProcessor:
    """Handles processing and transformation of parsed data."""
    
    def process_data(self, parsed_data: Dict[str, Any], output_file: str = "processed_data.csv") -> pd.DataFrame:
        """
        Process parsed data and convert to DataFrame.
        
        Args:
            parsed_data: Dictionary containing character data
            output_file: Optional CSV file to save processed data
            
        Returns:
            pd.DataFrame: Processed data frame
        """
        try:
            logger.info("Starting data processing...")
            logger.debug(f"Input data structure: {type(parsed_data)}")
            logger.debug(f"First record sample: {next(iter(parsed_data.items())) if parsed_data else 'No data'}")
            
            # Convert nested dictionary structure to flat DataFrame format
            processed_records = []
            for char_name, char_data in parsed_data.items():
                # Log each character's data for debugging
                logger.debug(f"Processing character: {char_name}, Data: {char_data}")
                
                # Extract alt names from the alts list
                alt_names = []
                for alt in char_data['alts']:
                    if isinstance(alt, tuple):
                        alt_names.append(alt[1])
                    elif isinstance(alt, dict):
                        alt_names.append(alt['name'])
                
                record = {
                    'id': char_data['id'],
                    'main_character': char_name,
                    'class_name': char_data['class_name'],
                    'points_current': char_data['points']['current_with_twink'],
                    'points_earned': char_data['points']['earned_with_twink'],
                    'points_spent': char_data['points']['spent_with_twink'],
                    'alts': ', '.join(alt_names) if alt_names else ''
                }
                processed_records.append(record)
            
            processed_df = pd.DataFrame(processed_records)
            
            # Log DataFrame structure and sample data
            logger.debug(f"DataFrame columns: {processed_df.columns.tolist()}")
            logger.debug(f"DataFrame sample: {processed_df.head(1).to_dict('records')}")
            
            if output_file:
                processed_df.to_csv(output_file, index=False)
                logger.info(f"Processed data saved to {output_file}")
            
            logger.info(f"Processing completed. Records processed: {len(processed_records)}")
            return processed_df
            
        except Exception as e:
            logger.error(f"Data processing failed: {str(e)}", exc_info=True)
            raise
