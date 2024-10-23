import pandas as pd
import random
from prettytable import PrettyTable

def print_data(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Select 5 random rows from the CSV
    random_indices = random.sample(range(len(df)), 5)
    selected_rows = df.iloc[random_indices]

    # Create a PrettyTable instance
    table = PrettyTable()
    table.field_names = ["ID", "Main Character", "Alts", "Current Points"]

    # Add rows to the table
    for _, row in selected_rows.iterrows():
        main_id = row['id']
        main_character = row['main_character']
        
        # Convert the string representation of a list of tuples into a simple list of names
        alts = eval(row['alts'])  # Converts the string back to a list of tuples
        alt_names = ", ".join([alt[1] for alt in alts])  # Extract the second item (name) from each tuple

        current_points = row['points_current']

        # Add a row to the table
        table.add_row([main_id, main_character, alt_names, current_points])

    # Print the styled table
    table.align = "l"
    print(table)

# Run the print_data function (example usage)
csv_file = "aggregated_dkp_points_with_separation.csv"  # Path to your CSV file
print_data(csv_file)
