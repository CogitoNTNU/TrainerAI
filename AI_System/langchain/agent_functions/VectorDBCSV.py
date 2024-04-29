from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
from dotenv import load_dotenv
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from datetime import datetime

unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
print(unix_timestamp)

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
    search_query: str = Field("You can search for exercise name, equipment required or muscle group. The input is a plain string, without curly brackets. By default use the string 'exercise'. Never input anything empty.")
@tool("search_exercises_vectorDB", args_schema=search_exercises_vectorDB_parameters)
def search_exercises_vectorDB(search_query: str = None):
    """A function for finding known exercises before adding them to a workout. Can also be used to find exercises that require specific equipment, or exercises that hit specific muscle groups. You can search in general for 'exercises'."""
    if(search_query == None):
        search_query = "exercise"

    print(search_query)
    embeddings = OpenAIEmbeddings()
    current_dir = os.getcwd()
    os.chdir("./vectorDB")
    new_exercises = FAISS.load_local("exercises",embeddings,allow_dangerous_deserialization=True)
    results = new_exercises.similarity_search(search_query,10)
    os.chdir(current_dir)
    return results



@tool("create_completed_workouts_vectorDB")
def create_completed_workouts_vectorDB():
    """Creates and updates the vector database of completed workouts."""
    current_dir = os.getcwd()
    embeddings = OpenAIEmbeddings()
    #list all completed wokout files
    directory = './workouts'
    all_workouts = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for i in all_workouts:
        print(all_workouts[i])
        datetime_str = all_workouts.split(".")[0] # remove filename ending
        print(datetime_str)
        format_str = "%Y%m%d_%H%M%S_%f" # Format the filename is in.
        datetime_object = datetime.strptime(datetime_str, format_str) # create datetime object. Using the format_str as a template to read.
        unix_timestamp = datetime_object.timestamp() # Convert to unix timestamp
        if all_workouts[i] >= unix_timestamp:
            all_workouts.remove(all_workouts[i])
    #create vDB of all workouts
    all_workouts = CSVLoader(file_path=all_workouts[0])
    loaded_workouts = workouts.load()
    workouts = FAISS.from_documents(loaded_workouts, embeddings)
    for i in all_workouts:
        temp_workout = CSVLoader(file_path=all_workouts[i])
        temp_workouts = temp_workout.load()
        workouts = FAISS.add_documents(temp_workouts, embeddings)
    os.chdir("./vectorDB")
    workouts.save_local("completed_workouts")
    os.chdir(current_dir)
    return print("Vector completed vectorDB created")

@tool("create_future_workouts_vectorDB")
def create_future_workouts_vectorDB():
    """Creates a vector database of future or planned workouts."""
    current_dir = os.getcwd()
    embeddings = OpenAIEmbeddings()
    #list all completed wokout files
    directory = './workouts'
    all_workouts = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for i in all_workouts:
        if all_workouts[i] < unix_timestamp:
            all_workouts.remove(all_workouts[i])
    #create vDB of all workouts
    all_workouts = CSVLoader(file_path=all_workouts[0])
    loaded_workouts = workouts.load()
    workouts = FAISS.from_documents(loaded_workouts, embeddings)
    for i in all_workouts:
        temp_workout = CSVLoader(file_path=all_workouts[i])
        temp_workouts = temp_workout.load()
        workouts = FAISS.add_documents(temp_workouts, embeddings)
    os.chdir("./vectorDB")
    workouts.save_local("future_workouts")
    os.chdir(current_dir)
    return print("future workouts vectroDB created")

class add_workout_to_a_vectorDB_parameters(BaseModel):
    vectorDB: str = Field("This should the name of the vector data base that the workout plan should be added to. This should be either 'completed_workouts' or 'future_workouts'.")
    workout_id: str = Field("The workout id should be a unique identifier for the workout plan.")
@tool("add_a_workout_to_a_vectorDB", args_schema=add_workout_to_a_vectorDB_parameters)
def add_a_workout_to_a_vectorDB(vectorDB: str, workout_id: str):
    """A function for adding a workout to a exsiting workout database."""
    try:
        assert vectorDB == "completed_workouts" or vectorDB == "future_workouts"
    except AssertionError:
        return print("The vectorDB should be either 'completed_workouts' or 'future_workouts'.")
    current_dir = os.getcwd()
    embeddings = OpenAIEmbeddings()
    os.chdir("./vectorDB")
    loaded_vectorDB = FAISS.load_local(vectorDB,allow_dangerous_deserialization=True)
    loaded_vectorDB.add_document(workout_id, embeddings)
    loaded_vectorDB.save_local(vectorDB)
    os.chdir(current_dir)
    return print(f'added {workout_id} to vector database: {vectorDB}')
                 
class search_workout_vectorDB_parameters(BaseModel):
    vectorDB: str = Field("This should the name of the vector data base that the workout plan should be added to. This should be either 'completed_workouts' or 'future_workouts'.")
    search_query: str = Field("The search query should be a string that can be used to search for a workout plan.")
@tool("search_workout_vectorDB", args_schema=search_workout_vectorDB_parameters)
def search_workout_vectorDB(vectorDB: str, search_query: str):
    """A function for searching for through either completed workouts or completed workouts in a vector database."""
    try:
        assert vectorDB == "completed_workouts" or vectorDB == "future_workouts"
    except AssertionError:
            return print("The vectorDB should be either 'completed_workouts' or 'future_workouts'.")
    if search_query == None:
        return search_query == "exercise"
    embeddings = OpenAIEmbeddings()
    query = search_query
    current_dir = os.getcwd()
    os.chdir("./vectorDB")
    new_exercises = FAISS.load_local(vectorDB,embeddings,allow_dangerous_deserialization=True)
    results = new_exercises.similarity_search(query,10)
    os.chdir(current_dir)
    return results