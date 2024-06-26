const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const fs = require('fs')

app.use(bodyParser.json())
app.use(express.static('public'))
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html')
})

// Links, constants
llm_url = 'http://llm-service:3001/send_message'

requestResponseLLM = async (message, conversation_id) => {
    try {
      const res = await fetch(llm_url, {
        method: "post",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({
          message: message,
          conversation_id: conversation_id
        })
      });
      
      const jsonData = await res.json();
      console.log(jsonData)
      return jsonData
    } catch (err) {
      console.log(err); //can be console.error
    }
}

app.get('/clear_chat_history', async (req, res) => {
  try {
    const result = await fetch('http://llm-service:3001/delete_chat_log', {
      method: "get",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
    });
    console.log("chatlog cleared - node res.")
    res.json({message: "cleared"})
  } catch (err) {
    console.log(err); //can be console.error
    res.json({message: "server error"})
  }
})

app.post('/send_message', async (req, res) => {
    const message = req.body.message
    const conversation_id = req.body.conversation_id
    
    let aiResponse = await requestResponseLLM(message, conversation_id)
    messageLog.push(message)

    res.json({
      "aiResponse": aiResponse,
      "messageLog": messageLog
    })
})

// TODO Setup a websocket connection for streaming results live.

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000')
})

messageLog = [] // History of the conversation