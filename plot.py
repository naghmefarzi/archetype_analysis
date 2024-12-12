import matplotlib.pyplot as plt
import numpy as np
import json
import argparse
import os

def load_data(file_path):
    """Load data from a JSONL file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]

def extract_numerical_data(data, data_labels):
    """Extract numerical data for roles, actions, and traits."""
    movie_labels = []
    numerical_data_roles = []
    numerical_data_actions = []
    numerical_data_traits = []

    for movie in data:
        for character, char_data in movie["actions_dict"].items():
            if 'numerical data' in char_data["roles"] and char_data["roles"]['numerical data'] != {}:
                # Add movie labels
                movie_labels.append(f"{movie} - {character}")
                
                # Collect numerical data for roles
                numerical_data_roles.append([char_data["roles"]["numerical data"].get(key, 0) for key in data_labels])
                
                # Collect numerical data for actions
                numerical_data_actions.append([char_data["actions"]["numerical data"].get(key, 0) for key in data_labels])
                
                # Collect numerical data for traits
                numerical_data_traits.append([char_data["traits"]["numerical data"].get(key, 0) for key in data_labels])

    # Convert numerical data to numpy arrays for easier plotting
    numerical_data_roles = np.array(numerical_data_roles)
    numerical_data_actions = np.array(numerical_data_actions)
    numerical_data_traits = np.array(numerical_data_traits)

    return movie_labels, numerical_data_roles, numerical_data_actions, numerical_data_traits

def plot_graphs(data, data_labels, movie_labels, category_name, output_file):
    """Plot bar and line graphs for the given data."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 15), constrained_layout=True)

    # Bar graph subplot
    bar_width = 0.1
    index = np.arange(len(movie_labels))

    # Create bars for each data point (e.g., turn, merge_action_over_global, etc.)
    for i, data_label in enumerate(data_labels):
        ax1.bar(index + i * bar_width, data[:, i], bar_width, label=data_label)

    # Bar graph labels and formatting
    ax1.set_xlabel('Characters in Movies')
    ax1.set_ylabel('Numerical Data')
    ax1.set_title(f'Bar Graph - Numerical Data for {category_name.capitalize()} in All Movies')
    ax1.set_xticks(index + bar_width * (len(data_labels) - 1) / 2)
    ax1.set_xticklabels(movie_labels, rotation=45)  # Rotate x-tick labels
    ax1.legend()

    # Line (dotted) plot subplot
    for i, data_label in enumerate(data_labels):
        ax2.plot(index, data[:, i], marker='o', linestyle=':', label=data_label)

    # Line plot labels and formatting
    ax2.set_xlabel('Characters in Movies')
    ax2.set_ylabel('Numerical Data')
    ax2.set_title(f'Line Graph - Trends for {category_name.capitalize()} in All Movies')
    ax2.set_xticks(index)
    ax2.set_xticklabels(movie_labels, rotation=45)  # Rotate x-tick labels
    ax2.legend()

    # Save the plot to the specified file
    plt.savefig(f"./plots/{output_file}")
    plt.close()  # Close the plot after saving to free memory

def main(args):
    """Main function to load data, process, and generate plots."""
    data_labels = ["turn", "merge_action_over_global", "merge_global_over_action", "merge_new", "kept_separate", "used_from_existing_functions"]
    categories = ["roles", "actions", "traits"]

    # Load data
    data = load_data(args.file_path)

    # Extract numerical data for roles, actions, and traits
    movie_labels, numerical_data_roles, numerical_data_actions, numerical_data_traits = extract_numerical_data(data, data_labels)

    # Plot and save the graphs for each category
    plot_graphs(numerical_data_roles, data_labels, movie_labels, "roles", args.roles_output)
    plot_graphs(numerical_data_actions, data_labels, movie_labels, "actions", args.actions_output)
    plot_graphs(numerical_data_traits, data_labels, movie_labels, "traits", args.traits_output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and plot numerical data from JSONL file.")
    
    # Define command-line arguments
    parser.add_argument('file_path', type=str, help="Path to the input JSONL file")
    parser.add_argument('--roles_output', type=str, default="roles_plot.png", help="Output file name for the roles plot")
    parser.add_argument('--actions_output', type=str, default="actions_plot.png", help="Output file name for the actions plot")
    parser.add_argument('--traits_output', type=str, default="traits_plot.png", help="Output file name for the traits plot")
    
    # Parse arguments
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs("./plots", exist_ok=True)

    # Run the main function
    main(args)
