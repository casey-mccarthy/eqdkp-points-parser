import pandas as pd
import random
import argparse
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
        # Filter the DataFrame by character name
        filtered_row = df[df['main_character'].str.lower() == character_name.lower()]
        if not filtered_row.empty:
            row = filtered_row.iloc[0]
            add_row_to_table(table, row)
        else:
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display DKP Data")
    parser.add_argument("mode", choices=["top", "character", "random"], help="Mode of displaying data")
    parser.add_argument("value", help="Character name, top number, or random count")
    args = parser.parse_args()

    csv_file = "aggregated_dkp_points_with_separation.csv"  # Path to your CSV file

    if args.mode == "character":
        print_data(csv_file, character_name=args.value)
    elif args.mode == "top":
        print_data(csv_file, top=int(args.value))
    elif args.mode == "random":
        print_data(csv_file, random_count=int(args.value))
