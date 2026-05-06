const conversationId = 1;

const socket = new WebSocket(
    "ws://" + window.location.host + "/ws/chat/" + conversationId + "/"
);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += "<p><b>" + data.sender + ":</b> " + data.message + "</p>";
};

function sendMessage() {
    const input = document.getElementById("message-input");

    socket.send(JSON.stringify({
        message: input.value
    }));

    input.value = "";
}