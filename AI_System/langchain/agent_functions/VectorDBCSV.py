from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
from dotenv import load_dotenv
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool


load_dotenv(dotenv_path="AI_System/langchain/.env")
OPENAI_API_KEY: str = os.getenv(key="OPENAI_API_KEY")


def create_exercises_vectorDB():
    exercises = CSVLoader(file_path="./exercises.csv")
    loaded_exercises = exercises.load()
    embeddings = OpenAIEmbeddings()
    exercises = FAISS.from_documents(loaded_exercises, embeddings)
    exercises.save_local("vector_exercises")

class search_exercises_vectorDB_parameters(BaseModel):
    search_query: str = Field("String to search for similar exercises in a vector DB")
@tool("search_exercises_vectorDB", args_schema=search_exercises_vectorDB_parameters)
def search_exercises_vectorDB(search_query: str):
    """A function for searching for exercises, and exercise details in the vector database. When looking for exercises to create workouts, or details about exercises, use this function. You can find required equipment, and muscle groups."""
    if search_query == None:
        return search_query == "exercises"
    embeddings = OpenAIEmbeddings()
    query = search_query
    new_exercises = FAISS.load_local("vector_exercises",embeddings)
    results = new_exercises.similarity_search(query,10)
    return results
