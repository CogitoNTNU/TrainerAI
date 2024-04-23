import pandas as pd

def create_workout_csv():
    workout = pd.DataFrame({"excercise":[],
                        "sets":[],
                        "reps":[],
                        "vekt":[],
                        "RPE":[]})
    workout.set_index("excercise",inplace=True)
    workout.to_csv("AI_System/langchain/workout.csv")
 
create_workout_csv()

def add_excercise_to_workout_plan(choose_exercise):
    workouts = pd.read_csv("AI_System/langchain/workouts.csv")
    workouts.set_index("exercise",inplace=True)
    print(workouts.index)
    print(workouts.index.dtype)
    workout = pd.read_csv("AI_System/langchain/workout.csv")
    workout.insert(0,choose_exercise, workouts.loc([[choose_exercise],["explenation"]]))
    
add_excercise_to_workout_plan("squat")

print(workout)

