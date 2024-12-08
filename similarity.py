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
import openai
from openai import OpenAI
import joblib
import os

# nlp = spacy.load("en_core_web_sm")
# word_vectors = api.load("word2vec-google-news-300")
# no_embeddings = set()


# def get_embedding(phrase):
#     doc = nlp(phrase)  
#     embeddings = []

#     for token in doc:
#         if not token.is_stop and not token.is_punct:  
#             try:
#                 embeddings.append(word_vectors[token.text.lower()]) 
#             except KeyError:
#                 if token.text not in no_embeddings:
#                     print(f"Warning: No embedding found for token '{token.text} in {phrase}'.")
#                     no_embeddings.add(token.text)
                
#                 continue  

#     return np.mean(embeddings, axis=0) if embeddings else np.zeros((300,)) 



# client = OpenAI(os.getenv("OPENAI_API_KEY"))

openai.api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI()

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


def get_embedding_efficient(text):
    embedding_cache = load_or_create_embedding_cache()
    if text in embedding_cache:
        return embedding_cache[text]
    else:
        embedding = get_embedding(text)
        embedding_cache[text] = embedding
        joblib.dump(embedding_cache, "/data/naghmeh/text-embedding-ada-002/word_embeddings.pkl")
        return embedding

def load_or_create_embedding_cache(filename="/data/naghmeh/text-embedding-ada-002/word_embeddings.pkl"):
    try:
        return joblib.load(filename)
    except FileNotFoundError:
        return {}



def argmax_cosine_sim(role, global_roles):
    role_embedding = get_embedding_efficient(role)
    max_similarity = 0
    most_similar_word = ""

    for global_role in global_roles:
        global_role_embedding = get_embedding_efficient(global_role)
        similarity = cosine_similarity([role_embedding], [global_role_embedding])[0][0]
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_word = global_role

    return most_similar_word


# print(argmax_cosine_sim("tutor", ["guide","sacrificer","protector"]))


def jaccard_similarity(roles1, roles2):
    mlb = MultiLabelBinarizer()
    binary_matrix = mlb.fit_transform([roles1, roles2])
    return jaccard_score(binary_matrix[0], binary_matrix[1], average='micro')

def old_cosine_sim(roles1, roles2):
    similarities = []
    for role1 in roles1:
        role1_vec = get_embedding_efficient(role1)
        max_sim = max([cosine_similarity([role1_vec], [get_embedding_efficient(role2)])[0][0] for role2 in roles2])
        similarities.append(max_sim)
    return np.max(similarities)


def cosine_sim(roles1, roles2):
    similarities = []
    for role1 in roles1:
        role1_vec = get_embedding_efficient(role1)
        max_sim = max([cosine_similarity([role1_vec], [get_embedding_efficient(role2)])[0][0] for role2 in roles2])
        similarities.append(max_sim)
    return np.mean(similarities)





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






def create_character_heatmap(movie_file_name,similarities, metric='Jaccard'):
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
    plt.savefig(f'./similarity_figs/character_similarity_heatmap{movie_file_name}_{metric}.png')
    plt.close()  

    # plt.show()


def sim_measure(movie_file_name):
    movies = load_movies(movie_file_name)
    similarities = compare_all_movies(movies)
    # Print similarities for each character comparison
    for movie_pair, char_similarities in similarities.items():
        print(f"\nComparisons for {movie_pair}:")
        for chars, sims in char_similarities.items():
            print(f"{chars}: Jaccard: {sims['Jaccard']:.3f}, Cosine: {sims['Cosine']:.3f}")

    save_similarities_to_csv(similarities, 'similarities.csv')
    create_character_heatmap(movie_file_name, similarities, metric='Jaccard')

    create_character_heatmap(movie_file_name, similarities, metric='Cosine')


# movie_file_name = '/extract_results/1k_movie_oct31.jsonl'
# sim_measure(movie_file_name)