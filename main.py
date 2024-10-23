import os
from dotenv import load_dotenv
from getpass import getpass
import logging
from rich.console import Console
from rich.prompt import Prompt
import pyfiglet



# Setup logging
logging.basicConfig(
    filename='main_script.log',
    filemode='w',  # Overwrites the file on each run
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def print_header():
    """Print a cool ASCII header using pyfiglet."""
    console = Console()
    ascii_art = pyfiglet.figlet_format("EQDKP Parser", font="slant")
    console.print(f"[bold cyan]{ascii_art}[/bold cyan]")

def check_env_file():
    """Check if the .env file exists and create one if not."""
    console = Console()

    if not os.path.exists(".env"):
        console.print("[yellow]No .env file found. Creating a new one...[/yellow]")
        with open(".env", "w") as env_file:
            env_file.write("API_KEY_CORE_READ=\n")
        logging.info("Created new .env file")

        # Prompt the user to set up their API key immediately
        api_key = getpass("Enter your API key: ").strip()
        with open(".env", "a") as env_file:
            env_file.write(f"API_KEY_CORE_READ={api_key}\n")
        logging.info("Added API key to .env file")
        
        console.print("[green]API key saved successfully to .env file![/green]")

def get_api_key():
    """Load the .env file and check for API key, prompt user if missing."""
    load_dotenv()
    api_key = os.getenv("API_KEY_CORE_READ")
    
    if not api_key:
        api_key = getpass("Enter your API key: ").strip()  # Use getpass to hide input for security
        with open(".env", "a") as env_file:
            env_file.write(f"API_KEY_CORE_READ={api_key}\n")
        logging.info("Added API key to .env file")
    return api_key


def main():
    console = Console()

    # Print the header
    print_header()

    # Step 1: Check for .env file and API key
    check_env_file()
    get_api_key()
    from fetch_points import fetch_points_data
    from parser import parse_dkp
    from print_data import print_data

    
    # Step 2: Run fetch function to get data
    console.print("[cyan]Fetching data from the API...[/cyan]")
    output_file = "response.xml"
    fetch_points_data(output_file)

    # Step 3: Parse the fetched data
    console.print("[cyan]Parsing the fetched data...[/cyan]")
    parse_dkp(output_file)

    # Step 4: Loop through print options
    console.print("[green]Data parsing complete. Entering print menu...[/green]")
    while True:
        console.print("[bold yellow]Options:[/bold yellow] [cyan]character <name>[/cyan] or [cyan]c <name>[/cyan], [cyan]top <number>[/cyan] or [cyan]t <number>[/cyan], [cyan]random <number>[/cyan] or [cyan]r <number>[/cyan], [cyan]exit[/cyan]")
        command = Prompt.ask("Enter command")
        if command.lower() == "exit":
            console.print("[bold green]Exiting program...[/bold green]")
            break
        try:
            if command.startswith("character ") or command.startswith("c "):
                _, character_name = command.split(" ", 1)
                print_data("aggregated_dkp_points_with_separation.csv", character_name=character_name)
            elif command.startswith("top ") or command.startswith("t "):
                _, number = command.split(" ", 1)
                print_data("aggregated_dkp_points_with_separation.csv", top=int(number))
            elif command.startswith("random ") or command.startswith("r "):
                _, number = command.split(" ", 1)
                print_data("aggregated_dkp_points_with_separation.csv", random_count=int(number))
            else:
                console.print("[bold red]Invalid command. Please try again.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]")
            logging.error(f"Error processing command '{command}': {e}")

if __name__ == "__main__":
    main()
