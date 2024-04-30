from flask import Flask, jsonify, request
import agent
from langchain_core.tracers.context import tracing_v2_enabled
from agent_functions.VectorDBCSV import create_exercises_vectorDB
import json
# AI Stuff
chatbot = agent.TrainAiChatbot()
def prompt_chatbot(prompt) -> str:
    # Code for tracking agent thought in langsmith
    try:
        with tracing_v2_enabled(project_name="default"):
            response = chatbot.run(prompt)
        return response
    except:
        return 'Something went wrong.'


#create_exercises_vectorDB()
create_exercises_vectorDB()
# Flask Stuff

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from LLM service!'
        
@app.route('/send_message', methods=['POST', 'GET'])
def llm_request():
    if(request.method == 'POST'):
        data = request.json
        print(data)
        print(data['message'])
        ai_message = prompt_chatbot(data['message'])
        return {"message": ai_message}

@app.route("/delete_chat_log", methods=["GET"])
def delete_chat_log():
    if(request.method == 'GET'):
        data = {"chat_history": []}
        file_path = 'chat_history.json'
        print("deleting chat history...")
        try:
            file = open(file_path, 'w')
            json.dump(data, file, indent=4)
            file.close()
            print("File has been overwritten with the new content.")
            return {"message": "OK"}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": f"An error occurred: {e}"}, 500
        return {"message": "OK"}

# main driver function
if __name__ == '__main__':
    app.run(debug=True, port=3001, host='0.0.0.0')