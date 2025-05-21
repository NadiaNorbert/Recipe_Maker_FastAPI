from fastapi import FastAPI
from pydantic import BaseModel
from retri import retrieve  # this is your context retriever
from chat import chat_completion  # this is your LLM caller

app = FastAPI()

class RecipeRequest(BaseModel):
    query: str

@app.post("/generate_recipe")
def generate_recipe(data: RecipeRequest):
    query = data.query
    context = retrieve("recipe", query) 

    prompt = f"""
You are a document expert. Answer the question based only on the provided context.

Context:
{context}

User Query:
{query}

Recipe:
"""

    result = chat_completion(prompt)

    if not result.strip():
        result = "Sorry, I couldn't find a recipe or generate a response."

    return {"response": result}
