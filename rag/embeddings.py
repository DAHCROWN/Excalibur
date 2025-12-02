# rag/embeddings.py

from typing import List
from pinecone import Pinecone
from google import genai
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_MODEL = "llama-text-embed-v2"  # Pinecone-hosted embedding model


class PineconeEmbeddingEngine:
    """
    Embedding engine using Pinecone's hosted embedding model.
    """

    def __init__(self, model_name: str = PINECONE_MODEL):
        if not PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY not set in environment variables.")
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.model_name = model_name
        

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using Pinecone's hosted embedding models.
        """
        try:
            print("---Received Text to Embed---")
            # print(f"Type: {type(texts)}")
            # print("Content")
            # print(texts)
            response = self.pc.inference.embed(
                model=self.model_name,
                inputs=texts,
                parameters={ "input_type": "passage", "truncate": "END"}
            )
            print("---------------------------")
            print("Embedding Successful")
            # print(response.data)
            return response.data
        except Exception as e:
            print(f"Failed to embed text, {texts[0]}")

class GeminiEmbeddingEngine:
    """
    Embedding engine using Gemini's hosted embedding model.
    """

    def __init__(self, model_name: str = "text-embedding-004"):
        self.model_name = model_name
        client = genai.Client()
        self.client = client
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using Gemini's hosted embedding models.
        """
        result = self.client.models.embed_content(
        model="gemini-embedding-001",
        contents="What is the meaning of life?")
