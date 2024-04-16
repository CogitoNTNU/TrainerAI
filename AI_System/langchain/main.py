from flask import Flask, jsonify, request

# Running on port 3001 - request not to localhost, but to "http://llm-service:3001"

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
        print(data)
        return {"message": "Hello, I'm your coach"}
    

# main driver function
if __name__ == '__main__':
    app.run(debug=True, port=3001, host='0.0.0.0')
