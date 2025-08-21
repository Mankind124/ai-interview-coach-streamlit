import streamlit as st
import PyPDF2
import io
import os
from services import interview_service
import speech_recognition as sr
from gtts import gTTS
import base64

# Page configuration
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .question-box {
        background: #e3f2fd;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    
    .feedback-box {
        background: #f1f8e9;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #8bc34a;
        margin: 1rem 0;
    }
    
    .audio-controls {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #ffeaa7;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .recording-indicator {
        color: #dc3545;
        font-weight: 600;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'step' not in st.session_state:
        st.session_state.step = 'upload'
    if 'candidate_name' not in st.session_state:
        st.session_state.candidate_name = ''
    if 'cv_text' not in st.session_state:
        st.session_state.cv_text = ''
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None
    if 'current_response' not in st.session_state:
        st.session_state.current_response = ''
    if 'audio_mode' not in st.session_state:
        st.session_state.audio_mode = False
    if 'sessions' not in st.session_state:
        st.session_state.sessions = {}
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ''

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def create_audio_player(text):
    """Create audio player for text-to-speech"""
    try:
        audio_bytes = interview_service.text_to_speech(text)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error(f"Audio generation failed: {e}")

def speech_to_text():
    """Convert speech to text using speech recognition"""
    try:
        r = sr.Recognizer()
        
        # Check if microphone is available
        mic_list = sr.Microphone.list_microphone_names()
        if not mic_list:
            st.error("❌ No microphones detected on your system")
            return None
        
        st.info(f"🎤 Using microphone: {mic_list[0]}")
        
        with sr.Microphone() as source:
            with st.spinner("🎤 Listening... Speak now!"):
                # More sensitive settings for Windows
                r.energy_threshold = 100  # Lower threshold for quieter sounds
                r.dynamic_energy_threshold = True
                r.pause_threshold = 1.5  # Longer pause detection (1.5 seconds of silence before stopping)
                
                # Quick ambient noise adjustment
                r.adjust_for_ambient_noise(source, duration=0.2)
                
                # Longer timeout and phrase limit for full responses
                audio = r.listen(source, timeout=10, phrase_time_limit=30)  # 30 seconds max recording
            
            with st.spinner("🔄 Processing speech..."):
                # Try Google first, then fallback
                try:
                    text = r.recognize_google(audio)
                    return text
                except:
                    # Fallback to Sphinx (offline) if available
                    try:
                        text = r.recognize_sphinx(audio)
                        return text
                    except:
                        raise sr.UnknownValueError()
                
    except sr.WaitTimeoutError:
        st.error("⏱️ No speech detected within 10 seconds. Please:")
        st.write("• Make sure your microphone is unmuted")
        st.write("• Try speaking RIGHT AFTER clicking the button") 
        st.write("• Speak clearly and loudly")
        st.write("• Check Windows microphone levels (should be 70-100%)")
        return None
    except sr.UnknownValueError:
        st.error("🤷 Could not understand audio. Please try:")
        st.write("• Speaking more clearly and slowly")
        st.write("• Moving closer to your microphone")
        st.write("• Reducing background noise")
        return None
    except sr.RequestError as e:
        st.error(f"❌ Speech Recognition service error: {e}")
        st.write("• Check your internet connection")
        return None
    except Exception as e:
        st.error(f"❌ Speech recognition error: {e}")
        st.write(f"Error details: {type(e).__name__}")
        return None

def main():
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Interview Coach</h1>
        <p>Practice your interview skills with AI-powered mock interviews</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 1: Upload and Setup
    if st.session_state.step == 'upload':
        st.header("📋 Get Started")
        
        # Candidate name input
        candidate_name = st.text_input(
            "👤 Your Name:",
            value=st.session_state.candidate_name,
            placeholder="Enter your full name"
        )
        st.session_state.candidate_name = candidate_name
        
        # CV upload
        st.subheader("📄 Upload Your CV/Resume")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt'],
            help="Upload your CV in PDF or text format"
        )
        
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                cv_text = extract_text_from_pdf(uploaded_file)
            else:
                cv_text = str(uploaded_file.read(), "utf-8")
            
            if cv_text:
                st.session_state.cv_text = cv_text
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
                # CV Preview
                with st.expander("👀 CV Preview"):
                    st.text_area("CV Content", cv_text[:500] + "...", height=200, disabled=True)
        
        # Audio mode toggle
        st.subheader("🎵 Audio Options")
        audio_mode = st.checkbox(
            "🎤 Enable Audio Mode",
            value=st.session_state.audio_mode,
            help="Enable speech-to-text input and text-to-speech output"
        )
        st.session_state.audio_mode = audio_mode
        
        if audio_mode:
            st.info("🔊 Audio mode enabled! You'll be able to speak your responses and hear questions read aloud.")
        
        # Start interview button
        if st.button("🚀 Start Mock Interview", disabled=not (candidate_name and st.session_state.cv_text)):
            session_id = interview_service.create_session(candidate_name, st.session_state.cv_text)
            st.session_state.session_id = session_id
            
            first_question = interview_service.generate_first_question(session_id)
            st.session_state.current_question = first_question
            st.session_state.step = 'interview'
            st.rerun()
    
    # Step 2: Interview
    elif st.session_state.step == 'interview':
        session = interview_service.get_session(st.session_state.session_id)
        
        if not session:
            st.error("Session not found. Please start a new interview.")
            st.session_state.step = 'upload'
            st.rerun()
            return
        
        st.header("🎯 Mock Interview Session")
        
        # Audio controls
        if st.session_state.audio_mode:
            st.markdown("""
            <div class="audio-controls">
                <p>🔊 Audio Mode Active</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Current question
        st.markdown(f"""
        <div class="question-box">
            <h3>🎤 Interviewer:</h3>
            <p>{session.current_question}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Audio player for question
        if st.session_state.audio_mode:
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🔊 Play Question"):
                    create_audio_player(session.current_question)
        
        # Response input section
        st.subheader("💬 Your Response")
        
        # Speech input
        if st.session_state.audio_mode:
            st.info("🎤 **Voice Recording Tips:** Click 'Record Response', then speak continuously. The recording will stop after 1.5 seconds of silence or 30 seconds max.")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("🎤 Record Response"):
                    speech_text = speech_to_text()
                    if speech_text:
                        st.session_state.current_response = speech_text
                        st.success(f"✅ Recorded: {speech_text[:100]}...")
            
            with col2:
                if st.button("🔧 Test Mic"):
                    st.info("Testing microphone...")
                    try:
                        import speech_recognition as sr
                        mic_list = sr.Microphone.list_microphone_names()
                        if mic_list:
                            st.success(f"✅ Found {len(mic_list)} microphone(s)")
                            for i, name in enumerate(mic_list[:3]):  # Show first 3
                                st.write(f"  {i+1}. {name}")
                            
                            # Test audio level
                            st.info("🔊 Testing audio level... Say something!")
                            r = sr.Recognizer()
                            with sr.Microphone() as source:
                                r.adjust_for_ambient_noise(source, duration=0.2)
                                st.write(f"🔇 Ambient noise level: {r.energy_threshold}")
                                
                                try:
                                    audio = r.listen(source, timeout=2, phrase_time_limit=2)
                                    st.success("✅ Audio captured successfully!")
                                except sr.WaitTimeoutError:
                                    st.warning("⚠️ No audio detected during test")
                        else:
                            st.error("❌ No microphones found")
                    except Exception as e:
                        st.error(f"❌ Microphone test failed: {e}")
        
        # Text input
        response = st.text_area(
            "💬 Type your response here (or use voice recording above):",
            value=st.session_state.current_response,
            height=150,
            placeholder="Share your thoughts and experiences...",
            help="You can type your response here if voice recording isn't working"
        )
        st.session_state.current_response = response
        
        # Quick suggestion
        if st.session_state.audio_mode and not response.strip():
            st.info("💡 **Tip:** If voice recording isn't working, you can type your response above and the app will still work perfectly!")
        
        # Submit response
        if st.button("➡️ Submit Response", disabled=not response.strip()):
            next_question = interview_service.generate_next_question(
                st.session_state.session_id, 
                response
            )
            
            if next_question == "INTERVIEW_COMPLETE":
                st.session_state.step = 'complete'
                st.rerun()
            else:
                st.session_state.current_question = next_question
                st.session_state.current_response = ''
                st.rerun()
    
    # Step 3: Feedback
    elif st.session_state.step == 'complete':
        st.header("🎉 Interview Complete!")
        
        feedback = interview_service.generate_feedback(st.session_state.session_id)
        
        st.markdown(f"""
        <div class="feedback-box">
            <h3>📊 Your Interview Feedback</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(feedback)
        
        # Audio feedback
        if st.session_state.audio_mode:
            if st.button("🔊 Listen to Feedback"):
                create_audio_player(feedback)
        
        # Reset for new interview
        if st.button("🔄 Start New Interview"):
            # Reset session state
            for key in ['step', 'candidate_name', 'cv_text', 'session_id', 'current_response', 'current_question']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()