const express = require('express')
const bodyParser = require('body-parser')

const app = express()
app.use(bodyParser.json())

app.use(express.static('public'))

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html')
})


requestResponseLLM = () => {
    (async () => {
        try {
          const res = await fetch('http://localhost:3000');
          const headerDate = res.headers && res.headers.get('date') ? res.headers.get('date') : 'no response date';
          console.log('Status Code:', res.status);
          console.log('Date in Response header:', headerDate);
      
          const jsonData = await res.json();
          return jsonData;
        } catch (err) {
          console.log(err.message); //can be console.error
        }
      })();
}

app.post('/send_message', (req, res) => {
    const data = req.body.message
    
    requestResponseLLM()

    messageLog.push(data)
    res.send(messageLog)
})

// TODO Setup a websocket connection for streaming results live.

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000')
})

messageLog = [] // History of the conversation