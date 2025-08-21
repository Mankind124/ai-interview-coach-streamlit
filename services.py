import openai
from typing import List, Dict
import uuid
from models import InterviewSession
import os
from dotenv import load_dotenv
import streamlit as st
import base64
import io

# Load environment variables
load_dotenv()

class InterviewService:
    def __init__(self):
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def _ensure_sessions_initialized(self):
        """Ensure sessions dictionary is initialized in session state"""
        if 'sessions' not in st.session_state:
            st.session_state.sessions = {}
    
    def create_session(self, candidate_name: str, cv_text: str) -> str:
        self._ensure_sessions_initialized()
        session_id = str(uuid.uuid4())
        session = InterviewSession(
            session_id=session_id,
            candidate_name=candidate_name,
            cv_text=cv_text
        )
        st.session_state.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> InterviewSession:
        self._ensure_sessions_initialized()
        return st.session_state.sessions.get(session_id)
    
    def generate_first_question(self, session_id: str) -> str:
        session = self.get_session(session_id)
        if not session:
            return "Session not found"
        
        prompt = f"""
        You are an experienced job interviewer. Based on the candidate's CV below, ask the first interview question.
        Make it a general opening question to get them comfortable.
        
        Candidate: {session.candidate_name}
        CV Summary: {session.cv_text[:1000]}...
        
        Ask ONE question only. Be professional and friendly.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            question = response.choices[0].message.content.strip()
            session.current_question = question
            session.questions_asked.append(question)
            return question
            
        except Exception as e:
            return f"Error generating question: {str(e)}"
    
    def generate_next_question(self, session_id: str, user_response: str) -> str:
        session = self.get_session(session_id)
        if not session:
            return "Session not found"
        
        session.responses.append(user_response)
        
        # Simple logic: ask 3 questions max
        if len(session.questions_asked) >= 3:
            return "INTERVIEW_COMPLETE"
        
        conversation_history = ""
        for i, (q, r) in enumerate(zip(session.questions_asked, session.responses)):
            conversation_history += f"Q{i+1}: {q}\nA{i+1}: {r}\n\n"
        
        prompt = f"""
        You are conducting a job interview. Based on the candidate's CV and previous responses, ask the next relevant question.
        
        Candidate: {session.candidate_name}
        CV: {session.cv_text[:800]}
        
        Previous conversation:
        {conversation_history}
        
        Ask ONE follow-up question that builds on their previous answers or explores a different aspect of their background.
        Be professional and engaging.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            question = response.choices[0].message.content.strip()
            session.current_question = question
            session.questions_asked.append(question)
            return question
            
        except Exception as e:
            return f"Error generating question: {str(e)}"
    
    def generate_feedback(self, session_id: str) -> str:
        session = self.get_session(session_id)
        if not session:
            return "Session not found"
        
        conversation_summary = ""
        for i, (q, r) in enumerate(zip(session.questions_asked, session.responses)):
            conversation_summary += f"Q{i+1}: {q}\nA{i+1}: {r}\n\n"
        
        prompt = f"""
        Provide interview feedback for this candidate based on their responses.
        
        Candidate: {session.candidate_name}
        
        Interview conversation:
        {conversation_summary}
        
        Provide:
        1. Overall performance summary
        2. Strengths demonstrated
        3. Areas for improvement
        4. Specific recommendations
        
        Keep it constructive and helpful.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating feedback: {str(e)}"

    def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech using gTTS"""
        try:
            from gtts import gTTS
            import io
            
            tts = gTTS(text=text, lang='en', slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer.getvalue()
        except Exception as e:
            st.error(f"Error generating speech: {e}")
            return None

# Global service instance
interview_service = InterviewService()