import pandas as pd
import matplotlib.pyplot as plt
from langchain.tools import StructuredTool


def time_calculate_total_minutes_from_csv_file__minute_column(csv_file_path, minute_column):
    df = pd.read_csv(csv_file_path)
    return df[minute_column].sum()

def check_if_x_>_y(x, y):
    return x > y

def multiply_x_by_y(x, y):
    return x * y



tools: list[StructuredTool] = [
    StructuredTool.from_function(
        name= "Check if x > y",
        func=check_if_x_>_y,
        description="Get the weather at a location given a latitude and longitude.",
    ),
    StructuredTool.from_function(
        name= "multiply x by y",
        func= multiply_x_by_y,
        description="Get average temperature from a list of temperatures",
    ),
]