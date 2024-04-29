import os
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool

@tool("listAllExistingWorkouts", return_direct=False)
def list_all_existing_workouts():
    """A function to retrieve all workout IDs of the user. Their name is the date and time they were created. Useful when having to display a large number of workouts, and to see the schedule, or a list of finished or planned workouts."""
    workouts = []
    # Find all workout files in the folder workouts
    directory = './workouts'
    workouts = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return workouts