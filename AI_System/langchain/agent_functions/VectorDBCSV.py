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
    exercises = CSVLoader(file_path="AI_System/langchain/exercises.csv")
    loaded_exercises = exercises.load()
    embeddings = OpenAIEmbeddings()
    exercises = FAISS.from_documents(loaded_exercises, embeddings)
    os.chdir("AI_System/langchain/vectorDB")
    exercises.save_local("exercises")

create_exercises_vectorDB()
embeddings = OpenAIEmbeddings()

class search_exercises_vectorDB_parameters(BaseModel):
    search_query: str = Field("The search query is the excersice, equipment, trainingtype etc, muscle group you want to search for in the vector database")
@tool("search_exercises_vectorDB", args_schema=search_exercises_vectorDB_parameters)
def search_exercises_vectorDB(search_query: str):
    """A function for searching for exercises in the vector database"""
    query = search_query
    os.chdir("./vectorDB")
    new_exercises = FAISS.load_local("exercises",embeddings)
    results = new_exercises.similarity_search(query,10)
    return results