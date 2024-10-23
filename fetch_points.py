import requests
import os
import logging
from dotenv import load_dotenv
from rich.progress import Progress
from rich.console import Console

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
    filename='fetch_points.log',
    filemode='w',  # Overwrites the file on each run
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def fetch_points_data(output_file):
    console = Console()
    logging.info("Starting fetch_points_data function...")

    # Retrieve the API token from environment variables
    api_token = os.getenv('API_KEY_CORE_READ')
    if not api_token:
        error_message = "Error: API key not found in environment variables."
        console.print(f"[bold red]{error_message}[/bold red]")
        logging.error(error_message)
        return

    # Define the API URL with query parameters
    api_url = f"https://dkp.kwsm.app/api.php?function=points&atoken={api_token}&atype=api"

    try:
        # Display a progress bar using Rich
        with Progress(console=console, transient=True) as progress:
            task = progress.add_task("[cyan]Fetching points data...", total=100)

            # Make the GET request to the API
            response = requests.get(api_url)

            # Simulate progress completion
            for _ in range(100):
                progress.update(task, advance=1)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the response content to an XML file
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(response.text)
            success_message = f"Data successfully saved to {output_file}"
            console.print(f"[bold green]{success_message}[/bold green]")
            logging.info(success_message)
        else:
            error_message = f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}"
            console.print(f"[bold red]{error_message}[/bold red]")
            logging.error(error_message)

    except Exception as e:
        error_message = f"An error occurred: {e}"
        console.print(f"[bold red]{error_message}[/bold red]")
        logging.error(error_message)

# Output file path
output_file = "response.xml"

