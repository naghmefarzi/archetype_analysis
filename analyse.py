import os
import json
from collections import defaultdict

def get_last_line_jsonl(filepath):
    with open(filepath, 'r') as file:
        last_line = file.readlines()[-1]
    return json.loads(last_line)

def compare_lists(list1, list2):
    set1, set2 = set(list1), set(list2)
    intersection = set1.intersection(set2)
    jaccard_index = len(intersection) / len(set1.union(set2)) if set1 or set2 else 0
    return len(intersection), jaccard_index

def process_all_jsonl(directory):
    data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".jsonl"):
            filepath = os.path.join(directory, filename)
            last_line_data = get_last_line_jsonl(filepath)
            all_actions = last_line_data.get('all_actions', {})
            data[filename] = {
                'roles': all_actions.get('roles', []),
                'actions': all_actions.get('actions', []),
                'traits': all_actions.get('traits', [])
            }
    
    comparisons = {'roles': [], 'actions': [], 'traits': []}
    filenames = list(data.keys())
    
    for i in range(len(filenames)):
        for j in range(i + 1, len(filenames)):
            file1, file2 = filenames[i], filenames[j]
            for key in comparisons.keys():
                list1, list2 = data[file1][key], data[file2][key]
                intersection_size, jaccard_index = compare_lists(list1, list2)
                comparisons[key].append({
                    'files': (file1, file2),
                    'intersection_size': intersection_size,
                    'jaccard_index': jaccard_index
                })
    
    return comparisons

def print_comparison_results(comparisons):
    for key, results in comparisons.items():
        print(f"\nComparisons for {key.capitalize()}:")
        for result in results:
            file1, file2 = result['files']
            print(f"{file1} vs {file2} - Intersection: {result['intersection_size']} items, Jaccard Index: {result['jaccard_index']:.2f}")

# Directory containing the .jsonl files
directory = "./extract_results/gpt/"
comparisons = process_all_jsonl(directory)
print_comparison_results(comparisons)





def get_last_line_jsonl(filepath):
    """Reads the last line of a JSONL file and returns it as a dictionary."""
    with open(filepath, 'r') as file:
        last_line = file.readlines()[-1]
    return json.loads(last_line)

def process_all_jsonl(directory):
    """Processes all JSONL files in a directory to find common and unique items."""
    data = {}
    all_items = defaultdict(set)  

    for filename in os.listdir(directory):
        if filename.endswith(".jsonl"):
            filepath = os.path.join(directory, filename)
            last_line_data = get_last_line_jsonl(filepath)
            all_actions = last_line_data.get('all_actions', {})
            data[filename] = {
                'roles': set(all_actions.get('roles', [])),
                'actions': set(all_actions.get('actions', [])),
                'traits': set(all_actions.get('traits', []))
            }
            for key in ['roles', 'actions', 'traits']:
                all_items[key].update(data[filename][key])

    # Find common items across all files
    common_items = {key: set.intersection(*(d[key] for d in data.values())) for key in all_items.keys()}

    # Find unique items for each file compared to the combined set of others
    unique_items = {}
    for filename, file_data in data.items():
        unique_items[filename] = {}
        for key in file_data.keys():
            unique_items[filename][key] = file_data[key] - common_items[key]
    
    return common_items, unique_items

def print_comparison_results(common_items, unique_items):
    """Prints common and unique items for each attribute type."""
    print("\nCommon Items Across All Files:")
    for key, items in common_items.items():
        print(f"  {key.capitalize()}: {sorted(items)}")

    print("\nUnique Items for Each File:")
    for filename, attributes in unique_items.items():
        print(f"\n{filename}:")
        for key, items in attributes.items():
            print(f"  Unique {key.capitalize()}: {sorted(items)}")
            
common_items, unique_items = process_all_jsonl(directory)
print_comparison_results(common_items, unique_items)