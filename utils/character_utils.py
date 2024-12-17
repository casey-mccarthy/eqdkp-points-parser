from typing import Optional, Tuple
import pandas as pd

def find_character(data: pd.DataFrame, character_name: str) -> Optional[Tuple[str, float]]:
    """
    Find a character in the main characters or alts list of the data.

    Args:
        data: DataFrame containing character data.
        character_name: Name of the character to search for.

    Returns:
        A tuple of the character name and their current DKP points if found, otherwise None.
    """
    character_name_lower = character_name.lower()
    
    # First try exact match on main character
    main_char_match = data[data['main_character'].str.lower() == character_name_lower]
    if not main_char_match.empty:
        row = main_char_match.iloc[0]
        return row['main_character'], row['points_current']
    
    # Then check alts
    for _, row in data.iterrows():
        alt_list = row['alts'].split(', ') if row['alts'] else []
        if any(alt.lower() == character_name_lower for alt in alt_list):
            return row['main_character'], row['points_current']
    
    return None 