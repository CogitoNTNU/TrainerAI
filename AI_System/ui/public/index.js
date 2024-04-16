// Runs on inital startup, after window (html) has finished loading
init = () => {
    document.getElementById('send_button').addEventListener('click', sendMessage)
}
window.onload = init;

// Placeholder
conversation_id = 0

// When user sends a message (pressing send button) this funciton runs
sendMessage = async () => {
    let chat_text_field = document.getElementById('chat_input_text')
    const user_input = chat_text_field.value
    addUserMessage(user_input)
    
    // Send a message to node, which forwards to llm-service to get the response from the chatbot
    res = await fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: user_input, conversation_id, source: 'user',})
    })
    chat_text_field.value = ''
    let json = await res.json()
    addMessage(json.aiResponse.message)
    let chat_history = document.getElementById("chat_history")
    chat_history.scrollTop = chat_history.scrollHeight;
}

window.addEventListener('keydown', (event) => {
    if(event.key == "Enter" && !event.shiftKey){
        sendMessage()
    }
})

// For seeing formatted HTML in javascript files, this extension for VSCode is recommended:
// https://marketplace.visualstudio.com/items?itemName=pushqrdx.inline-html

addMessage = (message) => {
    let html = /*html*/`
    <li class = "chat_element">
        <img class="profile_picture" src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn2.iconfinder.com%2Fdata%2Ficons%2Fdiversity-avatars-vol-3%2F64%2Ffitness-instructor-personal-trainer-man-caucasian-512.png&f=1&nofb=1&ipt=44eb31e947e63ae3345ece5d1353dedc01d10040a556a0d2d50a3ee8eee6e987&ipo=images">
        <div class="chat_message_container">
            <div class="chat_message">${message}</div>
    </li>`
    document.getElementById('chat_history').innerHTML += html;
}

addUserMessage = (message) => {
    let html = /*html*/`
    <li class = "chat_element">
        <img class="profile_picture" src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftoppng.com%2Fpublic%2Fuploads%2Fpreview%2Fuser-account-management-logo-user-icon-11562867145a56rus2zwu.png&f=1&nofb=1&ipt=5314f437c2b8d23762941ef06df17a94034191b5759f8871931e3fb0def23aed&ipo=images">
        <div class="chat_message_container">
            <div class="chat_message">${message}</div>
    </li>`
    document.getElementById('chat_history').innerHTML += html;
}

buildRecievingMessage = async () => {

}

initialLoadMessages = () => {
    const chat_box = document.getElementById('chat_history')
    allChats = []
    chat_box.value = messageLog.join('\n')
}