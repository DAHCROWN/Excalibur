
from pinecone import Pinecone
from lib.pinecone import PINECONE_INDEX_NAME, PINECONE_API_KEY

def retrieve_similar_emails(query: str):
    """
    Retrieve similar emails from Vertex AI Vector Search using semantic search.
    Returns the top matches with metadata and similarity scores.
    """

    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)
    query_payload = {
        "inputs": {
            "text": query
        },
        "top_k": 3
    }

    results = index.search(
        namespace="__default__",
        query=query_payload
    )

    return results

# TODO Finish testing this
def test_rag_retrival():
    print("[RAG] Retrieving embeddings...")
    result = retrieve_similar_emails(" OF CONGO FORCES AND THEIR FOREIGN ALLIES ANGOLA AND ZIMBABWE,")
    print(result)

if __name__ == "__main__":
    test_rag_retrival()