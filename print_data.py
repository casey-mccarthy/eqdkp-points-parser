import pandas as pd
import random
from rich.table import Table
from rich.console import Console

def print_data(csv_file, character_name=None, top=None, random_count=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Create a Rich Table instance
    table = Table(title="Aggregated DKP Points")

    # Define the columns
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Main Character", style="magenta")
    table.add_column("Alts", style="green")
    table.add_column("Current Points", justify="right", style="red")

    if character_name:
        # Normalize character name for comparison
        character_name_lower = character_name.lower()

        # Try to find the character as a main character
        filtered_row = df[df['main_character'].str.lower() == character_name_lower]
        
        if not filtered_row.empty:
            # Found a match in main characters
            row = filtered_row.iloc[0]
            add_row_to_table(table, row)
        else:
            # Check if the character is an alt
            found = False
            for _, row in df.iterrows():
                alts = eval(row['alts'])  # Converts the string back to a list of tuples
                if any(alt_name.lower() == character_name_lower for _, alt_name in alts):
                    add_row_to_table(table, row)
                    found = True
                    break

            if not found:
                console = Console()
                console.print(f"[bold red]Character '{character_name}' not found![/bold red]")
                return
    elif top:
        # Get the top characters by current DKP
        top_rows = df.nlargest(top, 'points_current')
        for _, row in top_rows.iterrows():
            add_row_to_table(table, row)
    elif random_count:
        # Select random rows
        random_indices = random.sample(range(len(df)), random_count)
        selected_rows = df.iloc[random_indices]
        for _, row in selected_rows.iterrows():
            add_row_to_table(table, row)
    else:
        # Default: Select 5 random rows from the CSV
        random_indices = random.sample(range(len(df)), 5)
        selected_rows = df.iloc[random_indices]
        for _, row in selected_rows.iterrows():
            add_row_to_table(table, row)

    # Create a console and print the table
    console = Console()
    console.print(table)

def add_row_to_table(table, row):
    """Helper function to add a row to the Rich table."""
    main_id = str(row['id'])
    main_character = row['main_character']
    
    # Convert the string representation of a list of tuples into a simple list of names
    alts = eval(row['alts'])  # Converts the string back to a list of tuples
    alt_names = ", ".join([alt[1] for alt in alts])  # Extract the second item (name) from each tuple

    current_points = str(row['points_current'])

    # Add a row to the Rich table
    table.add_row(main_id, main_character, alt_names, current_points)
