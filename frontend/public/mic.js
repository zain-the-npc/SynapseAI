let recognition;
let isListening = false;

function createMicButton() {
    const btn = document.createElement("button");
    btn.innerText = "🎤";
    btn.id = "mic-btn";

    btn.style.position = "fixed";
    btn.style.bottom = "20px";
    btn.style.right = "20px";
    btn.style.padding = "12px";
    btn.style.borderRadius = "50%";
    btn.style.fontSize = "20px";
    btn.style.backgroundColor = "#111";
    btn.style.color = "white";
    btn.style.border = "none";
    btn.style.cursor = "pointer";
    btn.style.zIndex = "9999";

    document.body.appendChild(btn);

    btn.onclick = toggleMic;
}

function toggleMic() {
    if (!('webkitSpeechRecognition' in window)) {
        alert("Speech Recognition not supported in this browser.");
        return;
    }

    if (!recognition) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onresult = function (event) {
            let transcript = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }

            // Send to Chainlit input box
            const textarea = document.querySelector("textarea");
            if (textarea) {
                textarea.value = transcript;
            }
        };
    }

    if (!isListening) {
        recognition.start();
        isListening = true;
        document.getElementById("mic-btn").style.backgroundColor = "red";
    } else {
        recognition.stop();
        isListening = false;
        document.getElementById("mic-btn").style.backgroundColor = "#111";

        // Auto send message
        const sendBtn = document.querySelector("button[type='submit']");
        if (sendBtn) sendBtn.click();
    }
}

window.addEventListener("load", createMicButton);