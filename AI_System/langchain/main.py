from flask import Flask, jsonify, request
import agent
from langchain_core.tracers.context import tracing_v2_enabled
from agent_functions.VectorDBCSV import create_exercises_vectorDB
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
    

# main driver function
if __name__ == '__main__':
    app.run(debug=True, port=3001, host='0.0.0.0')