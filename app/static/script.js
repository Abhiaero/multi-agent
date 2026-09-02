const messagesArea = document.getElementById('messagesArea');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

// A simple session ID for memory context
const sessionId = 'session_' + Math.random().toString(36).substr(2, 9);

function clearChat() {
    messagesArea.innerHTML = `
        <div class="message system-msg">
            <div class="msg-content">Chat history cleared. How can I help you?</div>
        </div>
    `;
}

function appendMessage(content, type, meta = null) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}-msg`;

    let innerHTML = `<div class="msg-content">${content}</div>`;
    
    // Add meta tags (Agent Used & Confidence) if provided
    if (meta && type === 'system') {
        const agentName = meta.agent_used.replace('_', ' ').toUpperCase();
        const confPercent = Math.round(meta.confidence * 100);
        const icon = meta.agent_used === 'rag_agent' ? 'database' : 
                     meta.agent_used === 'llm_agent' ? 'message-square' : 'shield-alert';
        
        innerHTML += `
            <div class="msg-meta">
                <span class="meta-tag ${meta.agent_used}">
                    <i data-lucide="${icon}" style="width: 12px; height: 12px;"></i>
                    ${agentName}
                </span>
                <span>${confPercent}% Confidence</span>
            </div>
        `;
    }

    msgDiv.innerHTML = innerHTML;
    messagesArea.appendChild(msgDiv);
    lucide.createIcons();
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

function showTypingIndicator() {
    const indicatorDiv = document.createElement('div');
    indicatorDiv.className = 'message system-msg';
    indicatorDiv.id = 'typingIndicator';
    indicatorDiv.innerHTML = `
        <div class="msg-content typing-indicator">
            <span></span><span></span><span></span>
        </div>
    `;
    messagesArea.appendChild(indicatorDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage(text, 'user');
    userInput.value = '';
    
    showTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: text, session_id: sessionId })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        removeTypingIndicator();
        appendMessage(data.response, 'system', {
            agent_used: data.agent_used,
            confidence: data.confidence
        });

    } catch (error) {
        removeTypingIndicator();
        appendMessage(`Sorry, something went wrong. (${error.message})`, 'system', {
            agent_used: 'fallback_agent',
            confidence: 0
        });
    }
}

// Event Listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
