const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const statusBadge = document.getElementById('backend-status');
const apiTokenInput = document.getElementById('api-token');
const backendUrlInput = document.getElementById('backend-url');

let isListening = false;
const recognition = window.SpeechRecognition || window.webkitSpeechRecognition ? new (window.SpeechRecognition || window.webkitSpeechRecognition)() : null;

if (recognition) {
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        userInput.value = text;
        sendMessage();
    };
    recognition.onend = () => {
        isListening = false;
        micBtn.style.color = 'var(--accent-color)';
    };
}

async function checkStatus() {
    try {
        const res = await fetch(`${backendUrlInput.value}/status`);
        if (res.ok) {
            statusBadge.innerText = 'LOCAL CONNECTED';
            statusBadge.className = 'online';
        } else {
            throw new Error();
        }
    } catch (e) {
        statusBadge.innerText = 'LOCAL DISCONNECTED';
        statusBadge.className = 'offline';
    }
}

function appendMessage(role, text, toolResult = null) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    
    let content = `<div class="content">${text}</div>`;
    if (toolResult) {
        content += `<div class="tool-badge">🔧 ${toolResult}</div>`;
    }
    
    msgDiv.innerHTML = content;
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.strip ? userInput.value.strip() : userInput.value.trim();
    if (!message) return;

    appendMessage('user', message);
    userInput.value = '';

    try {
        const res = await fetch(`${backendUrlInput.value}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                token: apiTokenInput.value
            })
        });

        const data = await res.json();
        if (data.error) {
            appendMessage('system', `Error: ${data.error}`);
        } else {
            appendMessage('ai', data.response, data.tool_result);
            // TTS Response
            if (window.speechSynthesis) {
                const utterance = new SpeechSynthesisUtterance(data.response);
                utterance.pitch = 0.9;
                utterance.rate = 1.0;
                window.speechSynthesis.speak(utterance);
            }
        }
    } catch (e) {
        appendMessage('system', 'Connection to J.A.R.V.I.S. backend failed.');
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

micBtn.addEventListener('click', () => {
    if (!recognition) {
        alert("Speech Recognition not supported in this browser.");
        return;
    }
    if (isListening) {
        recognition.stop();
    } else {
        isListening = true;
        micBtn.style.color = 'var(--danger)';
        recognition.start();
    }
});

// Periodic status check
setInterval(checkStatus, 5000);
checkStatus();
