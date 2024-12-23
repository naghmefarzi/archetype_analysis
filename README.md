# Archetype Analysis based on Character extraction and Action Extraction

This project analyzes characters and their associated actions in short stories or movie plots using a Generative AI model. It extracts character names and identifies their roles, providing insights into character interactions and narratives. then calculating the similarities between actions we aim to cluster characters with the goal of finding same archetypes.

Overview of the project:

![Overview](./Screenshot%202024-10-29%20at%2012.56.50%20PM.png)


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

Populate the data list in the main script with short stories formatted as dictionaries, or use a file containing that. Each dictionary should include:

"Title": The title of the story.
"Plot": The narrative text of the story.
"Characters": Optional.




The extracted character and action data will be saved in a JSON Lines file.



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
  "Character 1": {
      "roles": {
          "values": [
              "Role 1",
              "Role 2",
              "Role 3",
              "Role 4",
              "Role 5",
          ],
          "merging changes": [
              {
              "term": "role 1",
              "potential": "potential term from global list",
              "all existing list": [
                  "Role 1",
                  "Role 2",
                  "Role 3",
                  "Role 4",
                  "Role 5",

                ],
              "attribute type": "roles",
              "decision": "Keep Separate",
              "explanation": "rationale",
              "suggested term": "None"
            },
            ...],
            "numerical data": {
                    "turn":  1,
                    "merge_action_over_global": 0,
                    "merge_global_over_action": 0,
                    "merge_new": 0,
                    "kept_separate": 20,
                    "used_from_existing_functions": 0
                }
        },
    }
  }
  "all_actions": ["Action 1", "Action 2", ...]
}

The similarity then is being calculated using jaccard and embediing based cosine similarity, between then actions.





To run with gpt models:

First:
export OPENAI_API_KEY="your api key"

To run the program:

python main.py 
--model "gpt model" 
--output_path "jsonl output path" 
--temperature "gpt model temp" 
--seed "random seed" 
--merge

To make plots:

python plot.py 
"jsonl input file"
--roles_output name_of_the_roles_plot_file.png 
--actions_output name_of_the_roles_plot_file.png 
--traits_output name_of_the_roles_plot_file.png