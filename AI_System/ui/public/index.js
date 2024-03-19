messageLog = []

init = () => {
    console.log("Hello from the client side!")
    document.getElementById('send_button').addEventListener('click', sendMessage)
}

sendMessage = async () => {
    const user_input = document.getElementById('chat_input_text').value
    document.getElementById('chat_input_text').value = ''
    res = await fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: user_input, source: 'user' })
    })
    res.json().then(data => {
        console.log(data)
        messageLog = data
        renderMessages()
    })
}

renderMessages = () => {
    const chat_box = document.getElementById('chat_history')
    allChats = []
    chat_box.value = messageLog.join('\n')
}


window.onload = init;