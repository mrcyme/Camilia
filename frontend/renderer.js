let conversationId;

// Call this function to initiate conversation and get ID
function initiateConversation() {
    fetch('http://46.226.110.124:5000/initiate')
    .then(response => response.json())
    .then(data => {
        conversationId = data.conversation_id;
    });

}

function sendMessage() {
    const message = document.getElementById('input-message').value;
    const botType = document.getElementById('bot-type').value;
    const chatDiv = document.getElementById('chat-messages');
    chatDiv.innerHTML += `<div class="user-message">Cyme: ${message}</div>`;
    if (message && conversationId) {
        fetch('http://46.226.110.124:5000/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                conversation_id: conversationId,
                botType: botType
            })
        })
        .then(response => response.json())
        .then(data => {
            // Display message and response in chat UI
            console.log(data)
            const formattedResponse = data.message.replace(/\n/g, '<br>');
            chatDiv.innerHTML += `<div class="bot-message">CamilIA: ${formattedResponse}</div>`;
        });
    }
    document.getElementById('input-message').value = '';
}


document.getElementById('input-message').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});



// Initiate conversation on page load
window.onload = initiateConversation;
