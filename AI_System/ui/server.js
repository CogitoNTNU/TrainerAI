const express = require('express')
const bodyParser = require('body-parser')

const app = express()
app.use(bodyParser.json())

app.use(express.static('public'))

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html')
})

app.post('/send_message', (req, res) => {
    const data = req.body.message
    console.log(data)
    messageLog.push(data)
    res.send(messageLog)
})

// TODO Setup a websocket connection for streaming results live.

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000')
})

messageLog = []