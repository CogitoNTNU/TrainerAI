from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello from LLM service!'
 
# main driver function
if __name__ == '__main__':
    app.run(debug=True, port=3001, host='0.0.0.0')
