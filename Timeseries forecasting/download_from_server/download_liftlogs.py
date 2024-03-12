from pymongo import MongoClient
import os
import json
from dotenv import load_dotenv

# load environment variables
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
OWNER_ID = os.getenv('OWNER_ID')
client = MongoClient(MONGODB_URI)

# Query all liftlogs from a user
result = client['Jibe']['LiftLog'].find({
    'ownerId': OWNER_ID
})

# make a list of all exercises in the collection
unique_exercises = []
for doc in result:
    # load all exercises into a list from json
    exercises = doc['exercisesJson'] #json.loads(doc['exercisesJson'])
    for exercise in exercises:
        try:
            exercise_json = json.loads(exercise)
            if(exercise_json['exercise'] not in unique_exercises):
                unique_exercises.append(exercise_json['exercise'])
        except json.JSONDecodeError as e:
            print(f"Error decoding json: {e}, {exercise}")
print(unique_exercises)
print(f"{len(unique_exercises)} unique exercises found")

# create header 
result = client['Jibe']['LiftLog'].find({
    'ownerId': OWNER_ID
})

# save all results as a .csv file named data.csv
with open('volume.csv', 'w', encoding="utf-8") as f:
    header = "date,reps,sets,weightVolume"
    for exercise in unique_exercises:
        header += f",{exercise}"
    header += "\n"
    f.write(header)
    for doc in result:
        try:
            date = doc['dateTime']
            if date.microsecond > 0:
                date = date.replace(microsecond=0)
            exercises = doc['exercisesJson']
            reps = doc['reps']
            sets = doc['sets']
            weightVolume = doc['weightVolume']

            row = f"{date},{reps},{sets},{weightVolume}"

            for exercise_name in unique_exercises: # loads each exercise
                volume = 0 # total volume for this exercise
                for exercise in exercises:
                    exercise_json = json.loads(exercise)
                    if(exercise_json['exercise'] == exercise_name):
                        volume += float(exercise_json['weight']) * float(exercise_json['reps'])
                row += f",{volume}"

            row += "\n"
            f.write(row)
            
        except UnicodeEncodeError as e:
            print(f"Error writing to file: {e}, {doc}")

def calculateOneRepMax(W, R):
    epley = W * (1 + (R / 30))
    lombardi = W * R**0.10
    #mayhew = (100 * W) / (52.2 + (41.9 * e**(-0.055 * R)))
    oconner = W * (1 + (R / 40))
    if(R <= 10):
        brzycki = W * (36 / (37 - R))
        return (brzycki + epley + lombardi + oconner) / 4
    else:
        return (epley + lombardi + oconner) / 3

# create header 
result = client['Jibe']['LiftLog'].find({
    'ownerId': OWNER_ID
})

# save all results as a .csv file named data.csv
with open('onerepmax.csv', 'w', encoding="utf-8") as f:
    header = "date,reps,sets,weightVolume"
    for exercise in unique_exercises:
        header += f",{exercise}"
    header += "\n"
    f.write(header)
    for doc in result:
        try:
            date = doc['dateTime']
            if date.microsecond > 0:
                date = date.replace(microsecond=0)
            exercises = doc['exercisesJson']
            reps = doc['reps']
            sets = doc['sets']
            weightVolume = doc['weightVolume']

            row = f"{date},{reps},{sets},{weightVolume}"
            
            for exercise_name in unique_exercises: # loads each exercise
                onerepmax = 0
                for exercise in exercises:
                    exercise_json = json.loads(exercise)
                    if(exercise_json['exercise'] == exercise_name):
                        weight = float(exercise_json['weight'])
                        reps = float(exercise_json['reps'])
                        onerepmax = calculateOneRepMax(weight, reps)
                        # remove all but 2 digits
                        onerepmax = float(f"{onerepmax:.2f}")
                row += f",{onerepmax}"

            row += "\n"
            f.write(row)
            
        except UnicodeEncodeError as e:
            print(f"Error writing to file: {e}, {doc}")