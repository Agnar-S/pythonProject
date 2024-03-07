async function sendMessage() {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();

    if (message) {
        // Display user message
        const userDiv = document.createElement("div");
        userDiv.textContent = message;
        userDiv.className = "message user-message";
        chatBox.appendChild(userDiv);

        // Clear input
        userInput.value = "";

        // Send the message to the FastAPI backend and get the response
        try {
            const response = await fetch('http://127.0.0.1:8002/process-text/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: message }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();

            // Display bot message
            const botDiv = document.createElement("div");
            botDiv.textContent = result; // Assuming the response is just text. Adjust if your response structure is different.
            botDiv.className = "message bot-message";
            chatBox.appendChild(botDiv);

            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
        }
    }
}
