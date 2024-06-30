# tradelens

## Overview

TradeLens is an open-source trading journal tool designed to help traders gain deeper insights into their trades. By leveraging Obsidian, TradeLens offers a seamless way to convert trading data from HTS into structured notes.

## Features

- Import trading data directly from clipboard
- Automatically generate Obsidian-compatible markdown notes
- Track and analyze trade performance
- Easy to use and customizable

## Installation

1. Clone the repository:
    ```sh 
    git clone https://github.com/yourusername/tradelens.git
    cd tradelens
    ```

2. Create and activate a virtual environment using `poetry`:
    ```sh
    poetry install
    poetry shell
    ```

## Usage

1. Ensure your Kiwoom HTS trade log data is copied to the clipboard.

2. Run the CLI command to generate notes:
    ```sh
    python tradelens/main.py generate-notes --output-dir <output_directory>
    ```

    - `output-dir`: Directory where the generated markdown files will be saved.
    - `template-path` (optional): Path to the Jinja2 template file used for generating notes. Default is `tradelens/templates/journal_template.md`.

    Example:
    ```sh
    python tradelens/main.py generate-notes --output-dir notes
    ```