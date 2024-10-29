import requests
import json
from bs4 import BeautifulSoup

# URL of the TV Tropes page
url = "https://tvtropes.org/pmwiki/pmwiki.php/Main/TheEveryman"
archetype_name = url.split("/")[-1]

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

title = soup.find('title').text
print("Page Title:", title)

main_content = soup.find('div',{'id': 'main-article'})

scraped_text = []

# flg = False
movie_names = []
movie_links = []
all_text = []
link_url=link_text=""
for element in main_content.find_all(True):  # True gets all tags within the div
    tag_name = element.name
    element_id = element.get('id', 'No ID')  # Get the element's ID if it exists, otherwise 'No ID'
    element_classes = element.get('class', 'No Class')  # Get class, default 'No Class'
    element_href = element.get('href', 'No Href')  # Get href for links, if applicable
    element_src = element.get('src', 'No Src')  # Get src for images, if applicable
    
    # Get nested content
    nested_content = element.decode_contents()  # Get the content of the tag including nested tags
    
    # All attributes
    all_attributes = element.attrs  # Get all attributes as a dictionary
    
    if element.name == 'a':  # If it's a link
        link_text = element.text
        link_url = element['href']
        movie_links.append(f"Link: {link_text} ({link_url})")
    if element.name in ['i', 'em']:  # If it's italic text
        italic_text = element.text
        scraped_text.append(f"Italic: {italic_text}") ##Thats the movie name
        movie_names.append(italic_text)
        # if italic_text in link_url:
        #     movie_links.append(f"{link_text} ({link_url})")
    else:  # For regular text
        text = element.text.strip()
        if text:  # Avoid empty lines
            # if text == "Films — Live-Action":
                scraped_text.append(f"Tag: <{tag_name}> - Content: {text}")
                if tag_name=="li":
                    all_text.append((
            f"Tag: <{tag_name}> - ID: {element_id} - Classes: {element_classes} "
            f"- Href: {element_href} - Src: {element_src}  "
            f"- Nested Content: {nested_content} - Attributes: {all_attributes}"
            f"- Text: {text}"
            ))
j_data = {
    
    "archetype": archetype_name,
    "contents":all_text,
    "movie names": movie_names,
    "movie links": movie_links
    
}


with open(f"./{archetype_name}.json", "w") as f:
    json.dump(j_data, f, indent=4)  



# Print the results if needed
print("\n".join(scraped_text))