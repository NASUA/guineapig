document.addEventListener('DOMContentLoaded', function() {
    const talkButton = document.getElementById('talkButton');
    const responseTextElement = document.getElementById('responseText');

    // Check for browser support of the Web Speech API
    if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
        console.error('Your browser does not support the Web Speech API');
        responseTextElement.textContent = 'Your browser does not support speech recognition.';
        return; // Stop further execution if the API is not supported
    }

    // Initialize speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US'; // Set recognition language to English
    recognition.interimResults = false; // We only want final results

    recognition.onstart = function() {
        console.log('Speech recognition started');
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        responseTextElement.textContent = 'Sorry, I could not understand you.';
    };

    recognition.onend = function() {
        console.log('Speech recognition ended');
    };

    // Handle the result from speech recognition
    recognition.onresult = function(event) {
        const speechText = event.results[0][0].transcript;
        console.log('Recognized speech:', speechText);
        
        // Send the recognized speech text to the Flask backend
        fetch("/process_speech", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ speechText: speechText })
        })
        .then(response => response.json())
        .then(data => {
            if (data.translatedText) {
                responseTextElement.textContent = data.translatedText;
                convertTextToSpeech(data.translatedText, 'de'); // Assuming this function exists
            } else {
                responseTextElement.textContent = 'No translation available.';
            }
        })
        .catch(error => {
            console.error('Error during fetch:', error);
            responseTextElement.textContent = 'Sorry, there was an error processing your request.';
        });
    };

    // Attach the event listener to the talk button
    talkButton.addEventListener('click', () => {
        recognition.start(); // Start speech recognition
    });

    // Convert text to speech (assuming you have this functionality implemented)
    function convertTextToSpeech(text, lang) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang; // Set the language to Spanish
        speechSynthesis.speak(utterance);
    }
});
