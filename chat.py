from agno.agent import Agent
from agno.models.ollama import Ollama

# Initialize agent using Ollama model (make sure it's pulled via `ollama pull llama3`)
agent = Agent(
    model=Ollama(id="tinyllama"),
    markdown=True
)

def chat_completion(user_query: str):
    full_prompt = (
        "You are a document expert. Answer the question based on the document context only.\n\n"
        f"User: {user_query}"
    )

    response_text = ""
    response = agent.run(full_prompt, stream=True)

    for chunk in response:
        response_text += chunk.content  # Fix is here ✅

    return response_text
#print(chat_completion("How to make chole from the recipe?"))
