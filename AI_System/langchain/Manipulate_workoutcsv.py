import pandas as pd


workout = pd.DataFrame({"excercise":[],
                        "sets":[],
                        "reps":[],
                        "vekt":[],
                        "RPE":[],
                        "explenation":[]})
workout.set_index("excercise",inplace=True)
workout.to_csv("AI_System/langchain/workout.csv")
