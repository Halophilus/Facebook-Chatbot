# Facebook Data to Markov Model Generator - README

![Title](/docs/title.png)

## Overview
Facebook offers the ability to download all of their Facebook data in linked JSON files. This project aims to transform downloaded Facebook data into a Markov model to generate random statements based on everything the user has submitted in statuses, comments, and messages. It consists of two main components: the script for processing the data and the GUI for user interaction.

### Main Script
The script `main.py` contains several functions to handle Facebook data. Key functionalities include:

1. **Blacklist Handling**: Reads and applies a blacklist to filter out unwanted words.
2. **File Discovery**: Discovers and lists JSON files in a specified directory.
3. **Message Extraction**: Pulls messages from JSON files based on the sender's name.
4. **Alert Removal**: Filters out system alerts and non-original content from messages.
5. **Data Parsing**: Parses comments and statuses from JSON files.
6. **Markov Model Processing**: Processes data to create a word count dictionary for the Markov model and generates random statements.

### GUI Script
The `gui.py` script provides a Graphical User Interface using Tkinter. It allows users to:

- Enter their name for personalized data processing.
- Select outer directories containing Facebook data.
- Choose to include comments, statuses, and messages in the data processing.
- Check to see how many messages, statuses, or comments (if any) were found in the provided directory.
- Pull random entries from available data sources
- Generate random statements based on the selected data.
- Clear the output area.

![Name window](/docs/name.png)

![Main menu](/docs/main.png)

## Requirements
- Python 3.x
- Tkinter (usually comes with Python)
- Facebook data in JSON format

## Installation
1. Ensure Python 3.x is installed.
2. Download the project files to a local directory.
3. Place your Facebook data in a known directory.

## Usage
1. Run `gui.py` to start the application.
2. Enter your name in the pop-up window.
3. Use the "Get Directory" button to select the root directory of your Facebook data.
4. Select the types of data (Statuses, Comments, Messages) you want to include.
5. Click "GENERATE" to produce a random statement or set of statements based on the selected data.
6. Use the "CLEAR" button to clear the output area.

## Important Notes
- The project only processes data in the specified formats. Ensure your Facebook data is in the correct JSON format.
- The blacklist feature is crucial to filter out sensitive or unwanted content. Modify `filter.txt` as needed.

## License
This project is open-source and free for personal use. Please attribute the original creation appropriately in any derivative works.

