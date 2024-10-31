import json

def clean_jsonl(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        i = 0
        for line in infile:
            try:
                entry = json.loads(line)
                plot = entry.get("Plot")
                title = entry.get("Title")
                characters = entry.get("Characters")
                if plot is not None and title is not None and characters is not None and title!="" and plot!="" and characters!=[]:
                    title = title.strip()
                    plot = plot.strip()
                   
                
                if title and plot and isinstance(characters, list) and characters:
                    i+=1
                    outfile.write(json.dumps({
                        "Title": title,
                        "Plot": plot,
                        "character": characters
                    }) + "\n")
                    if i==1000:
                        break
            except json.JSONDecodeError:
                print("Invalid JSON entry detected and skipped.")

input_file = "/data/naghmeh/plots_146725_movies.jsonl"  
output_file = "/data/naghmeh/plots_1k_movies.jsonl" 


clean_jsonl(input_file, output_file)
print("Cleaning complete. Check the output file for results.")