# EQDKP Parser Project

This project is a DKP (Dragon Kill Points) parser that exports point data from an EQDKP data via XML files. It then aggregates and associates characters based on their main and alt designations and outputs this information in a clean and structured way using an interactive CLI.

## Example Output

Here's an example of the console output:

![Output](readme/example1.png)
![Output](readme/example2.png)

## Features

- **Interactive Command Line Interface**: Provides an interactive CLI for viewing data.
- **Fetch Data from API**: Securely fetches data from a remote API using an API key stored in an environment file.
- **Character Query**: Search for a character, their status, and their earned points.
- **Top N Characters**: View the top N characters by earned points.
- **Bidding Mode**: Allows users to enter a bidding mode to manage character bids interactively.

## Installation

Assuming you already have Python installed, follow these steps to set up the project:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/casey-mccarthy/eqdkp-points-parser.git
   ```

2. **Install Astral-UV**:
   Astral-UV is used for package management in this project. Install it using one of the following commands based on your operating system:

   - **On macOS/Linux**:
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```

   - **On Windows**:
     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

5. **Install dependencies and environment using Astral-UV**:
   ```bash
   uv sync
   ```

6. **Create a `.env` file**:
   If missing, the script will create a `.env` file and prompt you to set up your API key during runtime. The `.env` file should look like this:
   ```
   API_KEY=your_api_key_here
   ```
   This key can be located under your `Private API-Key` section of your profile on the EQDKP site.

## Usage

1. **Run the main script**:
   ```bash
   uv run run.py
   ```

2. **Follow the prompts** to set up your API key if required.

3. **Command Options**:
   After the data is fetched and parsed, you'll enter an interactive print menu. The following options are available:
   - **Character**:
     ```plaintext
     character <name> or c <name>
     ```
   - **Top N Characters**:
     ```plaintext
     top <number> or t <number>
     ```
   - **Enter Bidding Mode**:
     ```plaintext
     bid or b
     ```
   - **Exit**:
     ```plaintext
     exit or e
     ```

# Contribution Guidelines

We welcome contributions to the EQDKP Parser project! To maintain a clean and understandable commit history, please follow these guidelines when making contributions.

## Commit Message Tags

Use the following tags at the beginning of your commit messages to indicate the type of change you are making:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

## Example Commit Messages

- `feat: add new API endpoint for character data`
- `fix: resolve issue with data parsing`
- `docs: update README with contribution guidelines`
- `style: format code with black`
- `refactor: improve logging configuration`
- `perf: optimize database queries`
- `test: add unit tests for data fetcher`
- `chore: update dependencies`

## Versioning

We use [Semantic Versioning](https://semver.org/) for versioning. For the versions available, see the tags on this repository.

## How to Contribute

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -m 'feat: add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Open a pull request

Thank you for your contributions!

## Author

Created by Casey McCarthy.

## License

This project is open-source and available under the MIT License. 