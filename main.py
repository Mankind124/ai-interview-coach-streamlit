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
    if 'job_title' not in st.session_state:
        st.session_state.job_title = ''
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ''
    if 'company_name' not in st.session_state:
        st.session_state.company_name = ''
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
    if 'last_question_played' not in st.session_state:
        st.session_state.last_question_played = ''
    if 'feedback_played' not in st.session_state:
        st.session_state.feedback_played = False
    if 'auto_submit' not in st.session_state:
        st.session_state.auto_submit = False

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

def create_audio_player(text, auto_play=False):
    """Create audio player for text-to-speech with optional auto-play"""
    try:
        audio_bytes = interview_service.text_to_speech(text)
        if audio_bytes:
            if auto_play:
                # Auto-play the audio
                st.audio(audio_bytes, format="audio/mp3", autoplay=True)
            else:
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
                r.pause_threshold = 2.5  # Longer pause detection (2.5 seconds of silence before stopping)
                
                # Quick ambient noise adjustment
                r.adjust_for_ambient_noise(source, duration=0.2)
                
                # Much longer timeout and phrase limit for complete responses
                audio = r.listen(source, timeout=15, phrase_time_limit=60)  # 60 seconds max recording, 15 sec to start
            
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
        st.error("⏱️ No speech detected within 15 seconds. Please:")
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
        
        # Personal Information
        st.subheader("👤 Personal Information")
        candidate_name = st.text_input(
            "Your Name:",
            value=st.session_state.candidate_name,
            placeholder="Enter your full name"
        )
        st.session_state.candidate_name = candidate_name
        
        # Job Information
        st.subheader("💼 Job Information")
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input(
                "Job Title/Position:",
                value=st.session_state.job_title,
                placeholder="e.g., Software Engineer, Marketing Manager"
            )
            st.session_state.job_title = job_title
        
        with col2:
            company_name = st.text_input(
                "Company Name (Optional):",
                value=st.session_state.company_name,
                placeholder="e.g., Tech Corp, ABC Company"
            )
            st.session_state.company_name = company_name
        
        job_description = st.text_area(
            "Job Description:",
            value=st.session_state.job_description,
            height=120,
            placeholder="Paste the job description here. Include key responsibilities, requirements, and qualifications. This will help tailor the interview questions to the specific role.",
            help="The more detailed the job description, the more targeted your interview questions will be!"
        )
        st.session_state.job_description = job_description
        
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
        st.subheader("🎵 Interview Mode")
        audio_mode = st.checkbox(
            "🎤 Enable Audio Mode",
            value=st.session_state.audio_mode,
            help="Enable speech-to-text input and text-to-speech output"
        )
        st.session_state.audio_mode = audio_mode
        
        if audio_mode:
            st.info("🔊 **Audio Mode Features:**")
            st.write("• Questions will play automatically")
            st.write("• Voice recording with extended listening time (2.5 seconds pause, 60 seconds max)")
            st.write("• Automatic grammar correction and STAR analysis")
            st.write("• Natural conversation flow")
        else:
            st.info("💬 **Text Mode:** You can type responses and manually play audio if needed.")
        
        # Start interview button
        required_fields = candidate_name and st.session_state.cv_text and st.session_state.job_title
        
        if not required_fields:
            st.warning("⚠️ Please fill in your name, upload your CV, and specify the job title to start the interview.")
        
        if st.button("🚀 Start Mock Interview", disabled=not required_fields):
            session_id = interview_service.create_session(
                candidate_name, 
                st.session_state.cv_text,
                st.session_state.job_title,
                st.session_state.job_description,
                st.session_state.company_name
            )
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
        
        # Job context display
        job_info = f"**Position:** {session.job_title or 'Not specified'}"
        if session.company_name:
            job_info += f" | **Company:** {session.company_name}"
        st.info(f"🎯 {job_info}")
        
        # Progress indicator (without numbers for natural flow)
        progress = len(session.questions_asked) / 10
        st.progress(progress)
        progress_text = f"**Interview Progress:** {int(progress * 100)}% Complete"
        st.write(progress_text)
        
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
        
        # Auto-play question in audio mode
        if st.session_state.audio_mode:
            # Auto-play the current question when it's first displayed
            if 'last_question_played' not in st.session_state:
                st.session_state.last_question_played = ""
            
            if st.session_state.last_question_played != session.current_question:
                st.session_state.last_question_played = session.current_question
                with st.spinner("🔊 Playing question..."):
                    create_audio_player(session.current_question, auto_play=True)
                st.success("🔊 Question played automatically")
            
            # Manual play option
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🔊 Replay Question"):
                    create_audio_player(session.current_question)
        else:
            # Audio player for question (non-auto mode)
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🔊 Play Question"):
                    create_audio_player(session.current_question)
        
        # Response input section
        st.subheader("💬 Your Response")
        
        # STAR method guidance
        current_q_num = len(session.questions_asked)
        if 4 <= current_q_num <= 6:  # Behavioral questions
            with st.expander("⭐ STAR Method Guide", expanded=False):
                st.write("""
                **For behavioral questions, use the STAR method:**
                - **S**ituation: Set the context and background
                - **T**ask: Explain what needed to be accomplished  
                - **A**ction: Describe the specific actions you took
                - **R**esult: Share the outcomes and what you learned
                
                This helps provide complete, structured answers that interviewers love!
                """)
        
        # Speech input
        if st.session_state.audio_mode:
            st.info("🎤 **Voice Mode:** Record your response and it will be automatically submitted for processing!")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("🎤 Record Response"):
                    speech_text = speech_to_text()
                    if speech_text:
                        st.session_state.current_response = speech_text
                        st.success(f"✅ Recorded: {speech_text[:100]}...")
                        
                        # Auto-submit in audio mode
                        st.info("🔄 Auto-submitting your response...")
                        
                        # Trigger auto-submission by setting a flag
                        st.session_state.auto_submit = True
                        st.rerun()
            
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
            st.info("💡 **Tip:** Record your response using the microphone button above for automatic submission!")
        elif not st.session_state.audio_mode and not response.strip():
            st.info("💡 **Tip:** Type your response here, or enable audio mode for voice recording.")
        
        # Auto-submit logic for voice responses
        if st.session_state.get('auto_submit', False) and response.strip():
            st.session_state.auto_submit = False  # Reset flag
            
            with st.spinner("🔄 Auto-processing your voice response..."):
                # Automatic grammar correction (always applied)
                corrected_response = interview_service.correct_grammar(response)
                if corrected_response != response:
                    st.info("✨ **Grammar Assistant:** Your response has been automatically improved:")
                    with st.expander("View Changes", expanded=False):
                        st.write(f"**Original:** {response}")
                        st.write(f"**Improved:** {corrected_response}")
                
                # Generate next question
                next_question = interview_service.generate_next_question(
                    st.session_state.session_id, 
                    response
                )
                
                # Automatic STAR method feedback
                session = interview_service.get_session(st.session_state.session_id)
                if session and session.star_evaluations:
                    latest_star = session.star_evaluations[-1]
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("⭐ STAR Score", f"{latest_star.get('star_score', 0)}/10")
                    
                    with col2:
                        missing = latest_star.get('missing_elements', [])
                        if missing:
                            st.warning(f"💡 Consider adding: {', '.join(missing)}")
                        else:
                            st.success("✅ Great STAR structure!")
                
                if next_question == "INTERVIEW_COMPLETE":
                    st.session_state.step = 'complete'
                    st.success("🎉 Interview completed! Generating your feedback...")
                    st.rerun()
                else:
                    st.session_state.current_question = next_question
                    st.session_state.current_response = ''
                    
                    # Auto-play next question if audio mode is enabled
                    if st.session_state.audio_mode:
                        st.session_state.last_question_played = ""  # Reset to trigger auto-play
                    
                    st.success("✅ Voice response auto-submitted! Next question loading...")
                    if st.session_state.audio_mode:
                        st.info("🔊 Next question will play automatically...")
                    st.rerun()
        
        # Manual submit response (for text mode or manual submission)
        submit_disabled = not response.strip() or st.session_state.get('auto_submit', False)
        submit_label = "➡️ Submit Response" if not st.session_state.audio_mode else "➡️ Manual Submit (Optional)"
        
        if st.button(submit_label, disabled=submit_disabled):
            with st.spinner("🔄 Processing your response manually..."):
                # Automatic grammar correction (always applied)
                corrected_response = interview_service.correct_grammar(response)
                if corrected_response != response:
                    st.info("✨ **Grammar Assistant:** Your response has been automatically improved:")
                    with st.expander("View Changes", expanded=False):
                        st.write(f"**Original:** {response}")
                        st.write(f"**Improved:** {corrected_response}")
                
                # Generate next question
                next_question = interview_service.generate_next_question(
                    st.session_state.session_id, 
                    response
                )
                
                # Automatic STAR method feedback
                session = interview_service.get_session(st.session_state.session_id)
                if session and session.star_evaluations:
                    latest_star = session.star_evaluations[-1]
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("⭐ STAR Score", f"{latest_star.get('star_score', 0)}/10")
                    
                    with col2:
                        missing = latest_star.get('missing_elements', [])
                        if missing:
                            st.warning(f"💡 Consider adding: {', '.join(missing)}")
                        else:
                            st.success("✅ Great STAR structure!")
                
                if next_question == "INTERVIEW_COMPLETE":
                    st.session_state.step = 'complete'
                    st.success("🎉 Interview completed! Generating your feedback...")
                    st.rerun()
                else:
                    st.session_state.current_question = next_question
                    st.session_state.current_response = ''
                    
                    # Auto-play next question if audio mode is enabled
                    if st.session_state.audio_mode:
                        st.session_state.last_question_played = ""  # Reset to trigger auto-play
                    
                    st.success("✅ Response submitted! Next question loading...")
                    if st.session_state.audio_mode:
                        st.info("🔊 Next question will play automatically...")
                    st.rerun()
    
    # Step 3: Feedback
    elif st.session_state.step == 'complete':
        st.header("🎉 Interview Complete!")
        
        session = interview_service.get_session(st.session_state.session_id)
        
        # Show completion stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Questions Completed", f"{len(session.questions_asked)}/10")
        with col2:
            avg_star = sum([eval.get('star_score', 5) for eval in session.star_evaluations]) / len(session.star_evaluations) if session.star_evaluations else 5
            st.metric("Average STAR Score", f"{avg_star:.1f}/10")
        with col3:
            st.metric("Responses Given", len(session.responses))
        
        feedback = interview_service.generate_feedback(st.session_state.session_id)
        
        st.markdown(f"""
        <div class="feedback-box">
            <h3>📊 Your Comprehensive Interview Feedback</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(feedback)
        
        # Download feedback functionality
        col1, col2 = st.columns(2)
        with col1:
            # Create downloadable feedback
            feedback_text = f"""
AI Interview Coach - Feedback Report
=====================================

Candidate: {session.candidate_name}
Position: {session.job_title or 'Not specified'}
Company: {session.company_name or 'Not specified'}
Date: {st.session_state.get('interview_date', 'Today')}
Questions Completed: {len(session.questions_asked)}/10
Average STAR Score: {sum([eval.get('star_score', 5) for eval in session.star_evaluations]) / len(session.star_evaluations) if session.star_evaluations else 5:.1f}/10

{feedback}

---
Generated by AI Interview Coach
"""
            
            st.download_button(
                label="📥 Download Feedback",
                data=feedback_text,
                file_name=f"interview_feedback_{session.candidate_name.replace(' ', '_')}_{session.job_title.replace(' ', '_') if session.job_title else 'interview'}.txt",
                mime="text/plain",
                help="Download your interview feedback as a text file"
            )
        
        with col2:
            # Auto-play feedback in audio mode
            if st.session_state.audio_mode:
                if 'feedback_played' not in st.session_state:
                    st.session_state.feedback_played = False
                
                if not st.session_state.feedback_played:
                    st.session_state.feedback_played = True
                    with st.spinner("🔊 Playing feedback..."):
                        create_audio_player(feedback, auto_play=True)
                    st.success("🔊 Feedback played automatically")
                
                if st.button("🔊 Replay Feedback"):
                    create_audio_player(feedback)
            else:
                if st.button("🔊 Listen to Feedback"):
                    create_audio_player(feedback)
        
        # Reset for new interview
        if st.button("🔄 Start New Interview"):
            # Reset session state
            for key in ['step', 'candidate_name', 'cv_text', 'job_title', 'job_description', 'company_name', 
                       'session_id', 'current_response', 'current_question', 'last_question_played', 'feedback_played']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()