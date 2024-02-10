function sendMessage() {
    var inputElement = document.getElementById("userInput");
    var message = inputElement.value;

    var previous_chat_div = document.getElementById('chatContainer');
    var previous_messages = [];

    const kinder = previous_chat_div.childNodes;
    for (let i = 0; i < kinder.length; i++) {
      const child = kinder[i];
      if (child.innerHTML != null) {
          console.log(child.innerHTML);
          previous_messages.push(child.innerHTML);
      }
    }

    const message_object = {
      'kontext': previous_messages,
      'prompt': message
    };
    const jsonMessage = JSON.stringify(message_object);
    addToChat("User", message, "user-message");
    inputElement.value = "";

    fetch('/send/bot/message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: jsonMessage
    })
      .then(response => response.json())
      .then(data => {

        if (data['statistik'] != null) {
            var graph_path = data['statistik'];
            fetch('/graph/'+graph_path + '/' + JSON.stringify(data['kategorien']))
                .then(response => response.text())
                .then(imageString => {
                    var list = document.getElementById('graph_list');
                    var list_element = document.createElement('li');
                    var imgElement = document.createElement('img');
                    var delete_button = document.createElement('button');
                    delete_button.classList.add('deleteButton');
                    delete_button.innerHTML = 'X';
                    delete_button.addEventListener('click', deleteListItem);

                    imgElement.src = 'data:image/png;base64,' + imageString;
                    list_element.appendChild(imgElement);
                    list_element.appendChild(delete_button);
                    list.appendChild(list_element);

                    var botResponseText = data['antwort'];
                    addToChat("Bot", botResponseText, "bot-message");
                    var chatContainer = document.getElementById("chatContainer");
                    chatContainer.scrollTop = chatContainer.scrollHeight;
             });


        } else {
            var botResponseText = data['antwort'];
            addToChat("Bot", botResponseText, "bot-message");
            var chatContainer = document.getElementById("chatContainer");
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
      })

}


function clearChat() {
  var chatContainer = document.getElementById("chatContainer");
  chatContainer.innerHTML = "";
  var list = document.getElementById('graph_list');
  list.innerHTML = "";
}


function addToChat(sender, message, cssClass) {
    var chatContainer = document.getElementById("chatContainer");
    var messageElement = document.createElement("p");
    messageElement.classList.add(cssClass);
    messageElement.textContent = sender + ": " + message;
    chatContainer.appendChild(messageElement);
}

function deleteListItem() {
    var listItem = this.parentNode;
    listItem.parentNode.removeChild(listItem);
}