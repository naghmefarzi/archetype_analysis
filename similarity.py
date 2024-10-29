import json
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer
import gensim.downloader as api
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy

nlp = spacy.load("en_core_web_sm")
word_vectors = api.load("word2vec-google-news-300")
no_embeddings = set()

def jaccard_similarity(roles1, roles2):
    mlb = MultiLabelBinarizer()
    binary_matrix = mlb.fit_transform([roles1, roles2])
    return jaccard_score(binary_matrix[0], binary_matrix[1], average='micro')

def get_embedding(phrase):
    doc = nlp(phrase)  
    embeddings = []

    for token in doc:
        if not token.is_stop and not token.is_punct:  
            try:
                embeddings.append(word_vectors[token.text.lower()]) 
            except KeyError:
                if token.text not in no_embeddings:
                    print(f"Warning: No embedding found for token '{token.text} in {phrase}'.")
                    no_embeddings.add(token.text)
                
                continue  

    return np.mean(embeddings, axis=0) if embeddings else np.zeros((300,)) 


# Function to compute cosine similarity between two lists of roles
def cosine_sim(roles1, roles2):
    similarities = []
    for role1 in roles1:
        role1_vec = get_embedding(role1)
        max_sim = max([cosine_similarity([role1_vec], [get_embedding(role2)])[0][0] for role2 in roles2])
        similarities.append(max_sim)
    return np.max(similarities)

def compare_movies(movie1, movie2):
    char_similarities = {}
    for char1, roles1 in movie1['actions_dict'].items():
        for char2, roles2 in movie2['actions_dict'].items():
            jaccard_sim = jaccard_similarity(roles1, roles2)
            cosine_sim_value = cosine_sim(roles1, roles2)
            char_similarities[f"{char1} vs {char2}"] = {
                'Jaccard': jaccard_sim,
                'Cosine': cosine_sim_value
            }
    return char_similarities



def compare_all_movies(movie_data):
    all_similarities = {}
    num_movies = len(movie_data)

    # Loop over every pair of movies
    for i in range(num_movies):
        for j in range(i + 1, num_movies):  # Only compare each pair once
            movie1 = movie_data[i]
            movie2 = movie_data[j]
            comparison = compare_movies(movie1, movie2)
            all_similarities[f"{movie1['title']} vs {movie2['title']}"] = comparison

    return all_similarities






def load_movies(file_path):
    movies = []
    with open(file_path, 'r') as f:
        for line in f:
            movies.append(json.loads(line))
    return movies



movies = load_movies('character_actions_analysis_oct24_1.jsonl')
similarities = compare_all_movies(movies)
# Print similarities for each character comparison
for movie_pair, char_similarities in similarities.items():
    print(f"\nComparisons for {movie_pair}:")
    for chars, sims in char_similarities.items():
        print(f"{chars}: Jaccard: {sims['Jaccard']:.3f}, Cosine: {sims['Cosine']:.3f}")


def save_similarities_to_csv(similarities, filename):
    data = []
    for movie_pair, char_similarities in similarities.items():
        for chars, sims in char_similarities.items():
            data.append({
                'Movie Pair': movie_pair,
                'Character 1': chars.split('vs')[0],
                'Character 2': chars.split('vs')[1],
                'Jaccard': sims['Jaccard'],
                'Cosine': sims['Cosine']
            })
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

save_similarities_to_csv(similarities, 'similarities.csv')



def create_character_heatmap(similarities, metric='Jaccard'):
    heatmap_data = {}

    for movie_pair, char_similarities in similarities.items():
        for chars, sims in char_similarities.items():
            if sims[metric] > 0: 
                heatmap_data[chars] = sims[metric]

    heatmap_df = pd.DataFrame.from_dict(heatmap_data, orient='index', columns=[metric])

    plt.figure(figsize=(14, 12))
    sns.heatmap(heatmap_df, annot=True, cmap='coolwarm', fmt=".2f", cbar_kws={'label': metric})
    
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)

    plt.title(f'Character Similarity Heatmap ({metric})')
    plt.xlabel('Character Pairs')
    plt.ylabel('Similarity Score')

    # Save to file
    plt.tight_layout()  
    plt.savefig(f'character_similarity_heatmap_{metric}.png')
    plt.close()  

    # plt.show()

create_character_heatmap(similarities, metric='Jaccard')

create_character_heatmap(similarities, metric='Cosine')
