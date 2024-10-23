
# DKP Parser Project

This project is a DKP (Dragon Kill Points) parser that processes XML files containing player and point information for an online game. It aggregates and associates characters based on their main and alt designations and outputs this information in a clean and structured way.

## Features

- **Main and Alt Character Processing**: Identifies and separates main characters from their alts, ensuring alts are only processed after all mains have been identified.
- **Data Aggregation**: Collects point information including current, earned, spent, and adjusted points for each main character.
- **Flexible Data Output**: Outputs the results into a CSV file for easy viewing and sharing.
- **Pretty Print Table**: Provides a function to print the aggregated data in a nicely formatted table.
- **Logging**: Logs all processing steps, including when main characters and alts are associated.

## Data Model

The output data model is as follows:
- **id**: Main character's ID (integer).
- **main_character**: Main character's name (string).
- **alts**: List of tuples containing (ID, name) for each alt associated with the main character.
- **points**: A dictionary containing the following point values:
  - **earned**: Total points earned.
  - **spent**: Total points spent.
  - **adjusted**: Total points adjusted.
  - **current**: Current points.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Install dependencies**:
   ```bash
   pip install pandas prettytable
   ```

## Usage

1. **Parse the XML file**:
   Run the `parse_dkp` function to process an XML file and create a CSV:
   ```python
   parse_dkp("path/to/your/response.xml")
   ```

2. **Print random characters**:
   Use the `print_data` function to display 5 random main characters along with their associated alts and current points:
   ```python
   print_data("aggregated_dkp_points_with_separation.csv")
   ```

## Logging

Logs are stored in a file named `dkp_parser.log` in the project directory. The log captures all key steps and associations during processing.

## Example Output

Here’s an example of the CSV output and the printed table:

| ID  | Main Character | Alts                   | Points Earned | Points Spent | Points Adjusted | Points Current |
|-----|----------------|------------------------|---------------|--------------|-----------------|----------------|
| 56  | Dainae         | Berik, Byee, Cneasaigh | 3213          | 3543         | 520             | 190            |

```
+----+----------------+-------------------------------+----------------+
| ID | Main Character | Alts                          | Current Points |
+----+----------------+-------------------------------+----------------+
| 56 | Dainae         | Berik, Byee, Cneasaigh        | 190            |
| 78 | Avalansh       | Brogade, Vehho                | 114            |
| ...| ...            | ...                           | ...            |
+----+----------------+-------------------------------+----------------+
```

## Project Structure

```
/project-directory
│
├── dkp_parser.py         # Main script for parsing and CSV generation
├── print_data.py         # Script for displaying data in a formatted table
├── dkp_parser.log        # Log file capturing all processing steps
├── response.xml          # Example XML input file
└── README.md             # Project documentation
```

## Requirements

- **Python 3.x**
- **pandas** library
- **prettytable** library

## Author

Created by Casey McCarthy.

## License

This project is open-source and available under the MIT License.
