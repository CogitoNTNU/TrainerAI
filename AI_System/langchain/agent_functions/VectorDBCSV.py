from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
from dotenv import load_dotenv
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool


load_dotenv(dotenv_path="AI_System/langchain/.env")
OPENAI_API_KEY: str = os.getenv(key="OPENAI_API_KEY")


def create_exercises_vectorDB():
    current_dir = os.getcwd()
    exercises = CSVLoader(file_path="./exercises.csv")
    loaded_exercises = exercises.load()
    embeddings = OpenAIEmbeddings()
    exercises = FAISS.from_documents(loaded_exercises, embeddings)
    os.chdir("./vectorDB")
    exercises.save_local("exercises")
    os.chdir(current_dir)
    return print("Vector database created")


class search_exercises_vectorDB_parameters(BaseModel):
    search_query: str = Field("You can search for exercise name, equipment required or muscle group. The input can under no circumstances be empty.")
@tool("search_exercises_vectorDB", args_schema=search_exercises_vectorDB_parameters)
def search_exercises_vectorDB(search_query: str = None):
    """A function for finding known exercises before adding them to a workout. Can also be used to find exercises that require specific equipment, or exercises that hit specific muscle groups."""
    if search_query == None:
        return search_query == "exercise"
    embeddings = OpenAIEmbeddings()
    query = search_query
    current_dir = os.getcwd()
    os.chdir("./vectorDB")
    new_exercises = FAISS.load_local("exercises",embeddings,allow_dangerous_deserialization=True)
    results = new_exercises.similarity_search(query,10)
    os.chdir(current_dir)
    return results