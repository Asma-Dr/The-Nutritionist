import chromadb
from chromadb.utils import embedding_functions
import os

# Use a persistent path for the database
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")

def get_vector_store():
    """
    Returns the ChromaDB collection for nutrition data.
    """
    client = chromadb.PersistentClient(path=DB_DIR)
    
    # Use default Seed embedding function (all-MiniLM-L6-v2) by default if none specified
    # Chroma handles downloading the model automatically
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection = client.get_or_create_collection(
        name="nutrition_data",
        embedding_function=embedding_func
    )
    return collection
