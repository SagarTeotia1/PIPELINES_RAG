import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is required")
    
    # ChromaDB Configuration
    CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
    CHROMA_TENANT = os.getenv("CHROMA_TENANT")
    CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")
    
    if not all([CHROMA_API_KEY, CHROMA_TENANT, CHROMA_DATABASE]):
        raise ValueError("ChromaDB configuration is incomplete. Please set CHROMA_API_KEY, CHROMA_TENANT, and CHROMA_DATABASE")
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv("MONGODB_URI")
    if not MONGODB_URI:
        raise ValueError("MONGODB_URI environment variable is required")
    
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "rag_pipeline")
    MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "documents")
    
    # Application Configuration
    MAX_DOCUMENTS = int(os.getenv("MAX_DOCUMENTS", "20"))
    MAX_PAGES_PER_DOCUMENT = int(os.getenv("MAX_PAGES_PER_DOCUMENT", "1000"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
