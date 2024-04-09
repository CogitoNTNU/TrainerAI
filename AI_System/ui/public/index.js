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
        console.log(data[data.length-1])
        addUserMessage(data[data.length-1])
    })
}


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


window.onload = init;

buildRecievingMessage = async () => {

}

initialLoadMessages = () => {
    const chat_box = document.getElementById('chat_history')
    allChats = []
    chat_box.value = messageLog.join('\n')
}
