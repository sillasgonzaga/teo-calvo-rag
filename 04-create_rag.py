import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
SUMMARIES_FILES = 'data/ai_summaries.json'
SHORT_SUMMARIES_FILES = 'data/ai_short_summaries.json'

def load_data(file_path):
    with open(file_path, 'r') as file:
        video_data = json.load(file)
    return video_data


# Step 2: Generate embeddings for the summaries
def generate_embeddings(documents, model):
    summaries = [doc['summary'] for doc in documents]
    embeddings = model.encode(summaries)
    for i, doc in enumerate(documents):
        doc['embedding'] = embeddings[i]
    return documents




def get_user_input():
    # Get input from the user
    user_query = input("Sobre o que você quer aprender?\n\n")
    return user_query

def retrieve_videos(query, documents, model):
    # Generate embedding for the query
    query_embedding = model.encode([query])
    
    # Calculate cosine similarity between the query and document embeddings
    similarities = cosine_similarity(query_embedding, np.array([doc['embedding'] for doc in documents]))[0]
    
    # Rank documents based on similarity scores
    ranked_docs = sorted(zip(similarities, documents), reverse=True, key=lambda x: x[0])
    
    # Return top 5 results
    return [doc for _, doc in ranked_docs[:5]]

def generate_response(query, rag_documents, short_summaries, model):
    # Retrieve relevant videos
    relevant_videos = retrieve_videos(query, rag_documents, model)

    
    
    
    # Create a response with the video information
    response = f"Existem {len(relevant_videos)} vídeos que podem te ajudar a aprender sobre esse tema.\n\n"
    for vid in relevant_videos:
        video_id = vid['video_id']
        video_url = 'https://www.youtube.com/watch?v=' + video_id
        short_summary = short_summaries.get(video_id)
        # get only first 100 chars of summary
        #video_summary = vid['summary'][:100]
        response += f"Video URL: {video_url}\nSummary: {short_summary}\n\n"
    
    return response

def main():
    rag_documents = load_data(SUMMARIES_FILES)
    short_summaries_lst = load_data(SHORT_SUMMARIES_FILES)
    # transform short_summaries from a list of dicts to a single dict
    short_summaries_dct = {}
    for data in short_summaries_lst:
        short_summaries_dct[data['video_id']] = data['short_summary']


    print('Loading embedding model')
    rag_documents = generate_embeddings(rag_documents, model)
    

    # Get user input
    query = get_user_input()
    print('\n\n')
    
    # Generate response based on the query
    response = generate_response(query, rag_documents, short_summaries_dct, model)
    
    # Print the response
    print(response)

# Run the main function to start the interaction
if __name__ == "__main__":
    main()
