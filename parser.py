import xml.etree.ElementTree as ET
import pandas as pd

from main import LOGGER


def parse_dkp(xml_file: str) -> None:
    """
    Parses a DKP XML file and exports the data to a CSV file.

    This function processes an XML file containing player data, identifies main characters,
    associates alt characters with their respective main characters, and exports the aggregated
    data to a CSV file.

    Args:
        xml_file (str): The path to the XML file to be parsed.

    Returns:
        None

    Example Output:
        The function generates a CSV file with the following structure:
        - id: Main character's ID (integer)
        - main_character: Main character's name (string)
        - alts: List of tuples containing (ID, name) for each alt associated with the main character
        - points_earned: Total points earned
        - points_spent: Total points spent
        - points_adjusted: Total points adjusted
        - points_current: Current points

        Example row in CSV:
        {
            "id": 3547,
            "main_character": "Aacam",
            "alts": "[(4397, 'Aaeuvien'), (4010, 'Aafdular')]",
            "points_earned": 1000,
            "points_spent": 500,
            "points_adjusted": 50,
            "points_current": 550
        }
    """
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Get the list of players
    players = root.find("players")

    # Dictionary to store main characters and their associated data
    main_character_data: dict[str, dict] = {}

    # First Pass: Process and store all main characters
    LOGGER.info("Processing all main characters first...")
    for player in players.findall("player"):
        main_id = int(player.find("main_id").text)
        main_name = player.find("main_name").text
        char_id = int(player.find("id").text)
        name = player.find("name").text

        if main_id == char_id:  # Identify and add main characters only
            # Extract relevant point data with twinks
            points = player.find(".//multidkp_points")
            current_with_twink = int(points.find("points_current_with_twink").text)
            earned_with_twink = int(points.find("points_earned_with_twink").text)
            spent_with_twink = int(points.find("points_spent_with_twink").text)
            adjustment_with_twink = int(points.find("points_adjustment_with_twink").text)

            if main_name not in main_character_data:
                main_character_data[main_name] = {
                    "id": main_id,
                    "alts": [],
                    "points": {
                        "current": current_with_twink,
                        "earned": earned_with_twink,
                        "spent": spent_with_twink,
                        "adjusted": adjustment_with_twink
                    }
                }
                LOGGER.info(f"Main character added: {main_name} (ID: {main_id})")

    # Second Pass: Process all alt characters and associate them with their main characters
    for player in players.findall("player"):
        main_name = player.find("main_name").text
        char_id = int(player.find("id").text)
        name = player.find("name").text

        if main_name in main_character_data and main_name != name:  # Alt character association
            main_character_data[main_name]["alts"].append((char_id, name))
            LOGGER.info(f"Alt '{name}' (ID: {char_id}) associated with main '{main_name}'")
        elif main_name not in main_character_data:
            LOGGER.warning(f"Main character '{main_name}' not found for alt '{name}' (ID: {char_id})")

    # Prepare the final data structure for export and display
    final_data = []
    for main, data in main_character_data.items():
        final_data.append({
            "id": data["id"],
            "main_character": main,
            "alts": str([(alt_id, alt_name) for alt_id, alt_name in data["alts"]]),
            "points_earned": data["points"]["earned"],
            "points_spent": data["points"]["spent"],
            "points_adjusted": data["points"]["adjusted"],
            "points_current": data["points"]["current"]
        })

    # Create a DataFrame from the collected data
    df = pd.DataFrame(final_data)

    # Export to CSV
    df.to_csv("aggregated_dkp_points_with_separation.csv", index=False)
    
    # Log the completion of the task
    LOGGER.info("Aggregated DKP Points Table created and exported to CSV.")


