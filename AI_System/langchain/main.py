from flask import Flask, jsonify, request

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
from CustomDataLoader import get_csv_line

# Test
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
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


class TrainAiChatbot():
    def __init__(self) -> None:
        # Langchain setup
        LANGCHAIN_TRACING_V2: str = "true"
        # Language model
        self.llm: ChatOpenAI = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4-turbo")
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
        tools = [get_csv_line]
        llm = self.llm
        prompt = self.function_agent_prompt
        # Construct the OpenAI Functions agent
        agent = create_openai_functions_agent(llm, tools, prompt)

        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    def run(self, prompt: str) -> str:
        agent = self.create_function_agent_executor()
        output: str = agent.invoke({
        "input": f"{prompt}",
        "chat_history": self.get_chat_history(),
        })["output"]        
        self.save_history_chat(prompt, output)

        return output

    def get_chat_history(self) -> List[Union[HumanMessage, AIMessage]]:
        """
        A function for getting the chat history from a file
        """

        history: list = []
        chat_history_path = self.chat_history_path 
        
        with open(chat_history_path, "r") as f:
            data = json.load(f)
            for i in data["chat_history"]:
                history.append(HumanMessage(content=i["human_message"]))
                history.append(AIMessage(content=i["ai_message"]))
            f.close()
        
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

def prompt_chatbot(prompt) -> str:
    response = chatbot.run(prompt)
    return response

chatbot = TrainAiChatbot()

# All conversations will be stored in mongodb
example_conversation_data = [
    [
        {
            "agent": "user",
            "message": "help me make a workout",
        },
        {
            "agent": "ai",
            "message": "I can't",
        }
    ],
    [
        {
            "agent": "user",
            "message": "help me make a workout",
        },
        {
            "agent": "ai",
            "message": "No, go away",
        }
    ]
]

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from LLM service!'
        
@app.route('/send_message', methods=['POST', 'GET'])
def llm_request():
    if(request.method == 'GET'):
        # Placeholder for wrongful get request
        users = [{'id': 1, 'username': 'Alice'}, {'id': 2, 'username': 'Bob'}]
        return users
    if(request.method == 'POST'):
        data = request.json
        ai_message = prompt_chatbot(data['message'])
        return {"message": ai_message}
    

# main driver function
if __name__ == '__main__':
    app.run(debug=True, port=3001, host='0.0.0.0')
