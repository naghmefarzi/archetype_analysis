# Character Actions Analysis with Generative AI

This project analyzes characters and their associated actions in short stories using a Generative AI model. It extracts character names and identifies their roles through natural language processing, providing insights into character interactions and narratives.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Output Format](#output-format)

## Overview

The purpose of this project is to automate the extraction of character information and their actions from narrative texts. By leveraging a Generative AI model, the system generates responses to identify characters and their significant actions, allowing for comparative analysis across different stories.

## Requirements

- Python 3.x
- `gensim`
- `google-generativeai`
- `spacy`
- `json`
- `re`
- `time`
- `os`

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
Install the required packages:

pip install -r requirements.txt
Set up your API key for Google Generative AI:


export GEMINI_API_KEY='your_api_key_here'

Populate the data list in the main script with short stories formatted as dictionaries. Each dictionary should include:

"Title": The title of the story.
"Plot": The narrative text of the story.
"Characters": Optional.
Run the script:


python <script_name>.py
The extracted character and action data will be saved in a JSON Lines file named character_actions_analysis.jsonl.

Code Structure
UnitTests Class: Handles API calls to the Generative AI model to generate character and action data.

test_text_gen_text_only_prompt(prompt): Sends prompts to the AI model and retrieves generated content.
extract_characters_and_actions(ut, short_story, role_list): Analyzes the provided short story, extracting characters and identifying their roles through generated responses.

Main Execution: Loops through the data list, generates character and action data, and saves the results to a JSON Lines file.

Output Format
The output is saved in a JSON Lines format, where each line contains a JSON object with the following structure:


{
  "title": "Story Title",
  "plot": "The narrative text of the story.",
  "characters": ["Character 1", "Character 2", ...],
  "actions_dict": {
    "Character 1": ["Action 1", "Action 2", ...],
    "Character 2": ["Action 1", "Action 2", ...]
  },
  "all_actions": ["Action 1", "Action 2", ...]
}