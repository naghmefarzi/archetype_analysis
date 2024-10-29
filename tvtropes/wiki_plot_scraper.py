import requests
from bs4 import BeautifulSoup
import json

def get_wikipedia_plot(movie_name):
    base_url = "https://en.wikipedia.org/wiki/"
    url = base_url + movie_name.replace(' ', '_')
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the 'Plot' section header
        for header in soup.find_all(['h2', 'h3']):
            if 'Plot' in header.text:
                plot_text = []
                # Find the first element directly after the header
                element = header.find_next()
                while element and element.name not in ['h2', 'h3']:  # stop at next section
                    if element.name == 'p':  # append only paragraphs
                        plot_text.append(element.text)
                    element = element.find_next_sibling()
                return "\n".join(plot_text)
    return "Plot not found or page does not exist"


    
    

def read_jsonl(filename):

  data = []
  with open(filename, 'r') as f:
    text = f.read()
    data = json.loads(text)
  return data

# Example usage:
jsonl_data = read_jsonl("archetypes_movies.jsonl")
print(jsonl_data)

# Access data from the JSON objects:
for obj in jsonl_data:
  archetype_name = obj["archetype_name"]
  movies = obj["movies"]
  print(f"Archetype: {archetype_name}")
  new_movies = []
  for movie in movies:
      print(movie)
      d = {movie:get_wikipedia_plot(movie)}
      new_movies.append(d)
      
  obj['plots'] = new_movies
    # print(f"Movies: {movies}")
    

