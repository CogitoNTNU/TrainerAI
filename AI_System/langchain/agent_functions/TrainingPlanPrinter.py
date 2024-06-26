from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool

class standard_template_training_plan_printer_parameters(BaseModel):
    sets: int = Field(description="The amount of sets in the exercise")
    reps: int = Field(description="The amount of reps")
    weight: int = Field(description="Weight to be lifted")
    exercises: list[str] = Field(description="A list of the name of each exercise")

@tool("pretty_training_plan_printer", args_schema=standard_template_training_plan_printer_parameters)
def standard_template_training_plan_printer(sets: int, reps: int, weight: int, exercises: list[str]) -> str:
    """
    A function for printing a training plan. This function should ALWAYS be used to print any workoutplan, even when printing out more than one training plan in one output. The function takes in sets, reps and any amount of exercieses. Always use this function to display the modified workout, after modifying, or selecting exercises or workouts!!.
    """
    
    output: str = ""
    count: int = 1

    for exercise in exercises:
        print(exercise)
        output += f"{count}. {exercise}: {sets} sets x {reps} reps x {weight}"
        count += 1

    return output

if __name__ == "__main__":
    pass