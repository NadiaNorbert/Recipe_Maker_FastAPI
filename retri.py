from qdrant_client import QdrantClient
from openai import OpenAI
from chat import chat_completion
from agno.agent import Agent
from agno.models.ollama import Ollama

# Ollama agent
agent = Agent(
    model=Ollama(id="tinyllama"),
    markdown=True
)

def retrieve(COLLECTION_NAME, question):
    # Connect to Qdrant
    qdrant_client = QdrantClient(
        url="https://59004e01-863e-4d09-802b-24ddbcefe01b.eu-west-2-0.aws.cloud.qdrant.io:6333",
        api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.kEwGurfbzPq0Na9D1shINCrnqTjd5Q2DpT3EiKBzWeA",
    )

    # Set hybrid search models
    qdrant_client.set_model("sentence-transformers/all-MiniLM-L6-v2")
    qdrant_client.set_sparse_model("Qdrant/bm25")

    # Query for relevant chunks
    points = qdrant_client.query(
        collection_name=COLLECTION_NAME,
        query_text=question,
        limit=5,
    )

    
    final_points = ""

    for point in points:
        final_points += point.document

    # Final prompt with context
    prompt = f"""
You are a document expert. Answer the following question based only on the provided context.

Context:
{final_points}

Question: {question}
"""

    # Get answer from local LLM
    answer = chat_completion(prompt)
    return answer


# Example usage
#response = retrieve("recipe", "how to make chole")
#return response
#print(response)
