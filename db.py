import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import streamlit as st
import os

DB_DIR = os.path.join(os.path.dirname(__file__), "health_notes")  # Note: using underscore instead of hyphen

@st.cache_resource
def get_db():
    # Create directory if it doesn't exist
    os.makedirs(DB_DIR, exist_ok=True)
    
    # Initialize client with settings
    client = chromadb.PersistentClient(path=DB_DIR)
    
    # Use default embedding function instead of Ollama
    ef = embedding_functions.DefaultEmbeddingFunction()
    
    # Initialize collections
    for name in ["personal_data", "notes"]:
        try:
            client.get_or_create_collection(
                name=name,
                embedding_function=ef,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            st.error(f"Error creating collection {name}: {str(e)}")
            
    return client

# Initialize database connection
db = get_db()
personal_data_collection = db.get_collection("personal_data")
notes_collection = db.get_collection("notes")