# Basic langchain tools
import langchain
import langsmith
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Env variables
from config import OPENAI_API_KEY
from config import LANGSMITH_API_KEY

# Retrevial chain packages
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# History aware packages
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Custom modules
from CustomDocumentLoader import CustomDocumentLoader

# File manipulation
from agent_functions.Workout_CRUD import create_workout, read_workout, add_exercise_to_workout, delete_workout, remove_exercise_from_workout
from agent_functions.CSVLoadandRead import load_csv

# Training plan printer
from agent_functions.TrainingPlanPrinter import standard_template_training_plan_printer

# Functions
from agent_functions.listAllWorkoutFiles import list_all_existing_workouts
from agent_functions.generalFunctions import get_todays_time

# Test
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

# json file manipulation
import json

# Anotation
from typing import List, Union

# Env variables
from config import OPENAI_API_KEY
from config import LANGSMITH_API_KEY

# Running on port 3001 - request not to localhost, but to "http://llm-service:3001"

#midlirtigid bare for å sette fil lokasjon, bedre løsning må bli funnet
workouts_csv_location = "./workouts.csv"
workout_csv_location = "./workout.csv"


class TrainAiChatbot():
    def __init__(self) -> None:
        # Langchain setup
        LANGCHAIN_TRACING_V2: str = "true"
        # Language model
        self.llm: ChatOpenAI = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
        # Template prompt
        self.function_agent_prompt: ChatPromptTemplate = hub.pull("hwchase17/openai-functions-agent")
        # Path to chat history data
        self.chat_history_path: str = "chat_history.json"

    def create_function_agent_executor(self) -> AgentExecutor:
        """
        A function for creating an AI agent that is able to execute custom functions
        SUPER HELPFUL DOCUMENTATION: https://python.langchain.com/docs/modules/agents/agent_types/openai_functions_agent/
        """
        
        # The functions that the agent is able to use
        tools = [standard_template_training_plan_printer, 
                 create_workout,
                 read_workout,
                 add_exercise_to_workout,
                 remove_exercise_from_workout,
                 list_all_existing_workouts,
                 get_todays_time,
                 delete_workout]
        

        llm = self.llm
        prompt = self.function_agent_prompt
        # Construct the OpenAI Functions agent
        agent = create_tool_calling_agent(llm, tools, prompt)

        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    def run(self, prompt: str) -> str:
        agent = self.create_function_agent_executor()

        output: str = agent.invoke({
        "system": """You are a personal trainer, helping the user to reach their fitness goals.
        Your primary tasks are creating long-term workout plans, as well as detailed workouts for the user to execute. 
        You have access to a plethora of functions you can use to help the user. 
        You have access to chat history.
        Always use the standard_template_training_plan_printer when printing a workout plan. 
        workouts.csv file path is AI_System/langchain/workouts.csv and workout.csv
        file path is AI_System/langchain/workouts.csv""", # Relative paths should be handled by the functions alone.
        "input": f"{prompt}",
        "chat_history": self.get_recent_chat_history(max_pairs=20),
        })["output"]        
        self.save_history_chat(prompt, output)

        return output

    def get_recent_chat_history(self, max_pairs: int = 10) -> List[Union[HumanMessage, AIMessage]]:
        """
        Get a limited amount of messages

        Parameters:
        - max_pairs (int): The maximum number of message pairs to return.

        Returns:
        - history (List[Union[HumanMessage, AIMessage]]): A list of the most recent message pairs, up to the specified limit.
        """
        history: list = []
        chat_history_path = self.chat_history_path
        try:
            with open(chat_history_path, "r") as f:
                data = json.load(f)
                # Start from the end of the list and count backwards to get the most recent messages
                for i in reversed(data["chat_history"]):
                    # Prepend to history to maintain chronological order when output
                    history.insert(0, AIMessage(content=i["ai_message"]))
                    history.insert(0, HumanMessage(content=i["human_message"]))
                    # Check if we've collected enough pairs
                    if len(history) // 2 >= max_pairs:
                        break
        except FileNotFoundError:
            pass  # If the file doesn't exist, we simply return an empty history
        # Ensure that we return only the requested number of pairs
        return history[:max_pairs * 2]  # Each pair includes two messages



    def get_chat_history(self) -> List[Union[HumanMessage, AIMessage]]:
        """
        A function for getting the chat history from a file
        """
        history: list = []
        chat_history_path = self.chat_history_path 
        try:
            with open(chat_history_path, "r") as f:
                data = json.load(f)
                for i in data["chat_history"]:
                    history.append(HumanMessage(content=i["human_message"]))
                    history.append(AIMessage(content=i["ai_message"]))
                f.close()
        except FileNotFoundError:
            return history
        
        return history
    
    def save_history_chat(self, HumanMessage, AIMessage) -> None:
        """
        A function for saving the chat history
        """

        chat_history_path = self.chat_history_path 

        try:
            with open(chat_history_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            # If the file does not exist, create a new structure
            data = {"chat_history": []}
        except json.JSONDecodeError:
            # If the file is empty or corrupted, start fresh
            data = {"chat_history": []}

        new_entry = {
            "human_message": HumanMessage,
            "ai_message": AIMessage
        }

        data['chat_history'].append(new_entry)

        #Write the modified data back to the file
        with open(chat_history_path, "w") as file:
            json.dump(data, file, indent=4)  # Use indent for pretty-printing

