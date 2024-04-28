import pandas as pd
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_community.document_loaders.csv_loader import CSVLoader
import os

# importable tools from workout excercise loader
# set_workouts_csv_location
# set_workout_csv_location
# create_workout_csv
# add_excercise_to_workout_plan
# add_sets_to_exercise
# add_reps_to_exercise
# add_weight_to_exercise
# add_RPE_to_exercise
# add_time_to_exercise
# add_rest_to_exercise

from datetime import datetime
unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()

class create_new_workout_parameters(BaseModel):   
    date: str = Field(description="The date when the workout should start. This could be now, in the future or in the past.")
    time: str = Field(description="The time when the workout should start. This could be now, in the future or in the past.")
@tool("create_new_workout", args_schema=create_new_workout_parameters, return_direct=False)
def create_workout(date: str, time: str):
    """This tool creates a new csv file for a new workout. With the columns exercise, sets, reps, vekt, RPE and explanation for exercises."""
    workout = pd.DataFrame({"exercise":[],
                            "sets":[],
                            "reps":[],
                            "weight":[],
                            "rest":[],
                            "RPE":[],
                            "time":[],
                            "explanation":[]})
    workout.set_index("exercise",inplace=True)
    # Get current date and time
    combined_datetime = f"{date} {time}"
    datetime_object = datetime.strptime(combined_datetime, "%Y-%m-%d %H:%M")
    # Format the datetime object to create a unique workout ID
    formatted_date_time = datetime_object.strftime("%Y%m%d_%H%M%S_%f")
    workout_id = formatted_date_time
    workout_file_path = "./workouts/" + workout_id + ".csv"
    workout.to_csv(workout_file_path)
    return ("created workout at " + workout_file_path + " successfully! It's ID is: " + workout_id)

class read_workout_parameters(BaseModel):   
    workout_id: str = Field(description="ID of the workout you want to load, read or display. Gives you workout details. It's a date-time string. Remember to ALWAYS show the user the exercise name, reps and weight.")
@tool("read_workout", args_schema=read_workout_parameters, return_direct=False)
def read_workout(workout_id:str):
    """reads and outputs the workout file as a print"""
    path = "./workouts/" + workout_id + ".csv"
    loader = CSVLoader(path)
    loaded_csv = loader.load()
    if(len(loaded_csv) < 1):
        return "The workout is empty. Sorry."
    return loaded_csv

class add_exercise_to_workout_parameters(BaseModel):
    workout_id: str = Field(description="The ID of the workout as a string. The ID is the filename of the workout, which is the date and time the workout was recoreded.")
    exercise: str = Field(description="The exercise you want to add to the workout plan.")
    sets: str = Field(description="The amount of sets to do for this exercise")
    reps: str = Field(description="The amount of repetitions to do this exercise")
    weight: str = Field(description="The amount of weight to lift for this exercise")
    rest: str = Field(description="How long you should rest after doing this exercise.")
    time: str = Field(description="The time it takes/took you to do this exercise.")
    explanation: str = Field(description="The explanation of the exercise. Found by querying for the exercise.")
@tool("add_exercise_to_workout", args_schema=add_exercise_to_workout_parameters, return_direct=False)
def add_exercise_to_workout(workout_id:str, exercise:str, sets:str, reps:str, weight:str, rest:str, time:str, explanation:str):
    "This function lets you add an exercise to a specific workout. It requires the workout ID/Name, and the exercise you want to add. RPE must be set by the user. Remember to ALWAYS query an exercise, using search_exercises_vectorDB before running this function, so you're sure you have the right data."
    # last inn workout
    csvLocation = "./workouts/"+workout_id+".csv"
    workout = pd.read_csv(csvLocation, index_col="exercise") # loads workout csv.
    # Legg til øvelsen i workout
    workout.loc[exercise,"explanation"] = explanation
    workout.loc[exercise,"sets"] = sets
    workout.loc[exercise,"reps"] = reps
    workout.loc[exercise,"weight"] = weight
    workout.loc[exercise,"rest"] = rest
    workout.loc[exercise,"time"] = time
    workout.rename(index={len(workout):exercise},inplace=True)    #endrer index til å være øvelsen
    workout.to_csv(csvLocation)       #lagrer workout.csv

    return "Added %s to workout %s" % (exercise, workout_id)

class remove_exercise_from_workout_parameters(BaseModel):
    workout_id: str = Field(description="The ID of the workout as a string. The ID is the filename of the workout, which is the date and time the workout was recoreded.")
    exercise: str = Field(description="The exercise name you want to REMOVE from the workout plan.")
@tool("remove_exercise_from_workout", args_schema=remove_exercise_from_workout_parameters, return_direct=False)
def remove_exercise_from_workout(workout_id:str, exercise:str):
    "This function lets you REMOVE an exercise from a specific workout. It requires the workout ID/Name, and the exercise you want to remove."
    # Hent kjente øvelser fra vektordatabase - Basert på "exercise"
    # foundExercise = ["bench","Pectoralis" "major","Triceps","benchpress"]

    # last inn workout
    # workout = pd.read_csv("./workouts/"+workout_id, index_col="exercise") # loads workout csv.

    # Legg til øvelsen i workout
    # workout.loc[exercise,"explanation"] = foundExercise           #legger til forklaringen til øvelsen
    # workout.rename(index={len(workout):exercise},inplace=True)    #endrer index til å være øvelsen
    # workout.to_csv(workout_csv_location)       #lagrer workout.csv

    return "Remove %s from workout %s" % (exercise, workout_id)


class delete_workout_parameters(BaseModel):   
    workout_id: str = Field(description="ID of the workout you want to delete. It's a date-time string. You should list all workouts to see if the deletion was successfull.")
@tool("delete_workout", args_schema=delete_workout_parameters, return_direct=False)
def delete_workout(workout_id:str):
    """Deletes the workout CSV file for the given workout ID."""
    path = "./workouts/" + workout_id + ".csv"  # Ensure the file has a .csv extension
    try:
        os.remove(path)  # Attempt to remove the file
        return "Workout deleted: %s" % workout_id
    except FileNotFoundError:
        return "File not found: %s" % path
    except Exception as e:
        return "An error occurred: %s" % str(e)
    


"""

Old functions being rewritten below:

"""

workout_csv_location = "./workout.csv"


class set_exercise_paramaters(BaseModel):
    exercise: str = Field(description="Should be the exercise you're modifying. This input should be a string with the name of the excercise from workouts.csv, where row/index should be the same as in the workout.csv file")
@tool("select_exercise", args_schema=set_exercise_paramaters, return_direct=False)
def select_exercise(exercise):
    """This function selects the exercise you're going to modify. Run this first. Without it, all other functions won't work. Run this before each new exercise you're modifying."""
    global set_exercise
    set_exercise = exercise

class add_sets_to_excercise_paramaters(BaseModel):
    #exercise: str = Field(description="Should be the exercise you want to add to the workout plan, this input should be a string with the name of the excercise from workouts.csv, the row/index should be the same as in the workout.csv file")
    sets: str = Field(description="Should be the number of sets in the excerise")

@tool("add_sets_to_exercise", args_schema=add_sets_to_excercise_paramaters, return_direct=False)
def add_sets_to_exercise(sets:str):
    """adds sets to an exercise in the workout plan to the workout.csv file"""
    workout = pd.read_csv(workout_csv_location,index_col="exercise")  #åpner workout.csv
    workout.loc[set_exercise,"sets"] = sets   #legger til sets til øvelsen
    workout.to_csv(workout_csv_location)  #lagrer workout.csv

class add_reps_to_exercise_paramaters(BaseModel):
    #exercise: str = Field(description="Should be the exercise you want to add to the workout plan, this input should be a string with the name of the excercise from workouts.csv, the row/index should be the same as in the workout.csv file")
    reps: str = Field(description="Should be the number of reps in the excerise")

@tool("add_reps_to_exercise", args_schema=add_reps_to_exercise_paramaters, return_direct=False)
def add_reps_to_exercise(reps):
    """adds reps to an exercise in the workout plan to the workout.csv file"""
    workout = pd.read_csv(workout_csv_location,index_col="exercise")  #åpner workout.csv
    workout.loc[set_exercise,"reps"] = reps   #legger til reps til øvelsen
    workout.to_csv(workout_csv_location)  #lagrer workout.csv

class add_weight_to_exercise_paramaters(BaseModel):
    #exercise: str = Field(description="Should be the exercise you want to add to the workout plan, this input should be a string with the name of the excercise from workouts.csv, the row/index should be the same as in the workout.csv file")
    weight: int = Field(description="Should be the weight used for the excercise")

@tool("add_weight_to_exercise", args_schema=add_weight_to_exercise_paramaters, return_direct=False)
def add_weight_to_exercise(weight):
    """adds weight to an exercise in the workout plan to the workout.csv file"""
    if int(weight) == 0:
        weight = "bodyweight"
    elif int(weight) < 0:
        weight = "use bands or a diffrent way to make the excercise easier"
    workout = pd.read_csv(workout_csv_location,index_col="exercise")  #åpner workout.csv
    workout.loc[set_exercise,"weight"] = "%s kg" % weight   #legger til vekt til øvelsen
    workout.to_csv(workout_csv_location)  #lagrer workout.csv

class add_rest_to_exercise_paramaters(BaseModel):
    #exercise: str = Field(description="Should be the exercise you want to add to the workout plan, this input should be a string with the name of the excercise from workouts.csv, the row/index should be the same as in the workout.csv file")
    rest: int = Field(description="Should be the rest time between sets")

@tool("add_rest_to_exercise", args_schema=add_rest_to_exercise_paramaters, return_direct=False)
def add_rest_to_exercise(rest):
    """adds rest time time in minutes to an exercise based on the RPE of the excerscie in the workout plan to the workout.csv file"""
    workout = pd.read_csv(workout_csv_location,index_col="exercise")  #åpner workout.csv
    workout.loc[set_exercise,"rest"] = "%s min" % rest   #legger til rest til øvelsen
    workout.to_csv(workout_csv_location)

class workout_csv_paramaters(BaseModel):
    #exercise: str = Field(description="Should be the exercise you want to add to the workout plan, this input should be a string with the name of the excercise from workouts.csv, the row/index should be the same as in the workout.csv file")
    RPE: str = Field(description="Should be the RPE for the excercise, should be a number between 1 and 10 to set the precived intensity of the excercise")

@tool("add_RPE_to_exercise", args_schema=workout_csv_paramaters, return_direct=False)
def add_RPE_to_exercise(RPE):
    """adds RPE to an exercise in the workout plan to the workout.csv file"""
    if int(RPE) > 10:
        RPE == 10
    elif int(RPE) < 1:
        RPE == 1
    workout = pd.read_csv(workout_csv_location,index_col="exercise")  #åpner workout.csv
    workout.loc[set_exercise,"RPE"] = RPE   #legger til RPE til øvelsen
    workout.to_csv(workout_csv_location)  #lagrer workout.csv
class add_time_to_exercise_paramaters(BaseModel):
    #exercise: str = Field(description="Should be the exercise you want to add to the workout plan, this input should be a string with the name of the excercise from workouts.csv, the row/index should be the same as in the workout.csv file")
    time: int = Field(description="estimated time to complete reps and sets with estimated rest")

@tool("add_time_to_exercise", args_schema=add_time_to_exercise_paramaters, return_direct=False)
def add_time_to_exercise(time):
    """adds time in minutes to an exercise in the workout plan to the workout.csv file"""
    workout = pd.read_csv(workout_csv_location,index_col="exercise")  #åpner workout.csv
    workout.loc[set_exercise,"time"] = "%s min" % time
    workout.to_csv(workout_csv_location)

