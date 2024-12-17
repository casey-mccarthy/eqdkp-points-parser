from typing import Dict, List, Any
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

class DataProcessor:
    """Handles processing and transformation of parsed data."""
    
    def process_data(self, parsed_data: List[Dict[str, Any]], output_file: str = "processed_data.csv") -> pd.DataFrame:
        """
        Process parsed data and convert to DataFrame.
        
        Args:
            parsed_data: List of dictionaries containing character data
            output_file: Optional CSV file to save processed data
            
        Returns:
            pandas DataFrame containing processed data
        """
        logger.info("Processing parsed data...")
        
        df = pd.DataFrame(parsed_data)
        
        if output_file:
            df.to_csv(output_file, index=False)
            logger.info(f"Processed data saved to {output_file}")
            
        return df
