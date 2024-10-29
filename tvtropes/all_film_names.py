import requests
import time
from bs4 import BeautifulSoup
import requests
import json
import time
# Function to get the plot and cast of a movie from Wikipedia
def get_movie_info(movie_title):
    # Create a search URL
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={movie_title}&format=json"
    try:
        # Make a GET request to the Wikipedia API
        response = requests.get(search_url)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results for {movie_title}: {e}")
        return None, None  # Return None for both plot and cast

    # Check if we got a valid response
    if "query" in data and "search" in data["query"]:
        for result in data["query"]["search"]:
            # Get the page ID
            page_id = result['pageid']
            # Now get the plot and cast from the page
            info_url = f"https://en.wikipedia.org/w/api.php?action=parse&pageid={page_id}&prop=text&format=json"
            try:
                info_response = requests.get(info_url)
                info_data = info_response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching info for {movie_title} (page ID: {page_id}): {e}")
                continue  # Skip to the next movie if info fetch fails

            if "parse" in info_data:
                # Extract the HTML text and parse for the plot and cast
                info_html = info_data["parse"]["text"]["*"]
                
                # Use BeautifulSoup to parse the HTML
                soup = BeautifulSoup(info_html, 'html.parser')
                
                # Initialize empty strings to hold plot and cast text
                plot_text = ""
                cast_text = ""
                cast_texts = []
                # Flags to determine when we are in the desired sections
                in_plot_section = False
                in_cast_section = False
                for element in soup.find_all(['h2', 'h3', 'p', 'ul']):
                    # Check for headings indicating plot or cast sections
                    if element.name == 'h2' or element.name == 'h3':
                        if "Plot" in element.get_text() or "Synopsis" in element.get_text():
                            in_plot_section = True
                            in_cast_section = False  # Reset cast section
                        elif "Cast" in element.get_text():
                            in_cast_section = True
                            in_plot_section = False  # Reset plot section
                        else:
                            # If we hit another section and were in a plot or cast section, we stop
                            if in_plot_section or in_cast_section:
                                break  # Stop if we move on from the desired sections
                    
                    # If we're in the plot section, accumulate text from paragraph tags
                    if in_plot_section and element.name == 'p':
                        plot_text += element.get_text() + "\n"
                    
                    if in_cast_section and element.name == 'ul':
                        for li in element.find_all('li'):
                            # Check if the list item contains an <a> tag for the actor's name
                            a_tag = li.find('a')
                            if a_tag:
                                actor = a_tag.get_text()  # Actor's name from <a> tag
                            else:
                                actor = li.get_text().split(' as ')[0]  # Actor's name from plain text
                            # Extract the character name by splitting on ' as '
                            character_text = li.get_text()
                            if ' as ' in character_text:
                                character = character_text.split(' as ')[-1]
                                cast_texts.append(character)
                            else:
                                character = "Unknown Character"
                            
                    # print(cast_texts)
                # Clean up and return the plot and cast text
                return plot_text.strip() if plot_text else None, cast_texts
movies_path = "/data/naghmeh/data.txt"
movie_info = {}
with open(movies_path, "r") as file:
    lines = file.readlines()
total_movies = len(lines)
num = 1000
num = total_movies
step_size = max(total_movies // num, 1)  
for i in range(0, total_movies, step_size):
    movie_info_line = json.loads(lines[i].strip()) 
    title = movie_info_line["title"]
    print(f"Fetching info for: {title}")
    # Get the movie plot and cast
    try:
        plot, cast = get_movie_info(title)
        movie_info[title] = {'Plot': plot, 'Cast': cast}
    except:
        print(f"ERROR FOR info for: {title}")
    if len(movie_info) >= num:  
        break
    # Output the plots
    ents = []
    for title, info in movie_info.items():
        
        
        ent = {"Title": title,
        "Plot":info['Plot'] ,
        "Characters":info['Cast']
        }
        ents.append(ent)
        # print(ent)
    with open(f"/data/naghmeh/plots_{num}_movies.jsonl","w") as f:
        for ent in ents:
            json.dump(ent, f)  # Write each JSON object
            f.write("\n")  # Add a newline character after each JSON object