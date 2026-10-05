import os
from dotenv import load_dotenv  

load_dotenv()  
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_MODEL = "llama-text-embed-v2"  # Pinecone-hosted embedding model
PINECONE_INDEX_NAME = "fraud-email-index"