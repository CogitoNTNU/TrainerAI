import os
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from datetime import datetime

@tool("getTodaysTime", return_direct=False)
def get_todays_time():
    """A function to get the current date and time."""
    now = datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_date_time