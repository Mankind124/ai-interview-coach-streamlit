"""
Web Speech API Integration for Browser-based Speech Recognition
This allows speech recognition to work in cloud deployments
"""

import streamlit as st
import streamlit.components.v1 as components

def create_web_speech_component():
    """Create a web speech recognition component using browser APIs"""
    
    web_speech_html = """
    <div id="speech-container">
        <button id="start-speech" onclick="startRecording()" style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 0;
        ">🎤 Start Recording</button>
        
        <button id="stop-speech" onclick="stopRecording()" style="
            background: #e74c3c;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
            display: none;
        ">⏹️ Stop Recording</button>
        
        <div id="speech-status" style="margin: 10px 0; font-weight: bold;"></div>
        <div id="speech-result" style="
            border: 1px solid #ddd;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            min-height: 50px;
            background: #f9f9f9;
        "></div>
    </div>

    <script>
        let recognition;
        let isRecording = false;

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
            
            recognition.onstart = function() {
                document.getElementById('speech-status').innerHTML = '🎤 Listening... Speak now!';
                document.getElementById('start-speech').style.display = 'none';
                document.getElementById('stop-speech').style.display = 'inline-block';
                isRecording = true;
            };
            
            recognition.onresult = function(event) {
                let finalTranscript = '';
                let interimTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }
                
                document.getElementById('speech-result').innerHTML = 
                    '<strong>Final:</strong> ' + finalTranscript + 
                    '<br><em>Interim:</em> ' + interimTranscript;
                
                // Send result to Streamlit
                if (finalTranscript) {
                    window.parent.postMessage({
                        type: 'speech-result',
                        text: finalTranscript
                    }, '*');
                }
            };
            
            recognition.onerror = function(event) {
                document.getElementById('speech-status').innerHTML = '❌ Error: ' + event.error;
                resetButtons();
            };
            
            recognition.onend = function() {
                document.getElementById('speech-status').innerHTML = '✅ Recording completed';
                resetButtons();
            };
            
        } else {
            document.getElementById('speech-container').innerHTML = 
                '<p style="color: #e74c3c;">❌ Speech recognition not supported in this browser. Please use Chrome, Edge, or Safari.</p>';
        }

        function startRecording() {
            if (recognition && !isRecording) {
                recognition.start();
            }
        }

        function stopRecording() {
            if (recognition && isRecording) {
                recognition.stop();
            }
        }

        function resetButtons() {
            document.getElementById('start-speech').style.display = 'inline-block';
            document.getElementById('stop-speech').style.display = 'none';
            isRecording = false;
        }

        // Listen for messages from Streamlit
        window.addEventListener('message', function(event) {
            if (event.data.type === 'clear-speech') {
                document.getElementById('speech-result').innerHTML = '';
                document.getElementById('speech-status').innerHTML = '';
            }
        });
    </script>
    """
    
    return web_speech_html

def web_speech_recognition():
    """Browser-based speech recognition component"""
    
    st.subheader("🌐 Browser Speech Recognition")
    st.info("💡 **This uses your browser's built-in speech recognition - works in cloud deployment!**")
    
    # Create the web speech component
    web_speech_html = create_web_speech_component()
    
    # Display the component
    components.html(web_speech_html, height=200)
    
    # JavaScript to handle speech results
    components.html("""
    <script>
        // Listen for speech results
        window.addEventListener('message', function(event) {
            if (event.data.type === 'speech-result') {
                // Update Streamlit session state (this would need custom integration)
                console.log('Speech result:', event.data.text);
            }
        });
    </script>
    """, height=0)

if __name__ == "__main__":
    # Test the component
    st.title("Web Speech Recognition Test")
    web_speech_recognition()
