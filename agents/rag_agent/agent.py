from google.adk.agents.llm_agent import LlmAgent
from tools.rag_retriever_tool import retrieve_similar_emails


rag_retriever_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="rag_retriever_agent",
    description="Retrieves similar emails from the vector database using semantic search to compare new emails with known spam or phishing samples.",
    instruction="""You are a semantic search agent. 
    Given an email body, subject, or both, embed the text and use the retrieve_similar_emails tool 
    to search the Vertex Vector Store for similar known spam or phishing examples. 

    Return ONLY:
    - similarity score
    - matched email snippet
    - metadata fields: sender, subject, label, url count
    """,
    tools=[retrieve_similar_emails]
)