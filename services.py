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
    
    def create_session(self, candidate_name: str, cv_text: str, job_title: str = "", job_description: str = "", company_name: str = "") -> str:
        self._ensure_sessions_initialized()
        session_id = str(uuid.uuid4())
        session = InterviewSession(
            session_id=session_id,
            candidate_name=candidate_name,
            cv_text=cv_text,
            job_title=job_title,
            job_description=job_description,
            company_name=company_name
        )
        st.session_state.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> InterviewSession:
        """Get session by session_id"""
        self._ensure_sessions_initialized()
        return st.session_state.sessions.get(session_id)
    
    def correct_grammar(self, text: str) -> str:
        """Auto-correct grammar and improve clarity of user responses"""
        try:
            prompt = f"""
            You are a professional writing assistant. Please correct any grammatical errors, improve clarity, and maintain the original meaning of this interview response. Keep the tone professional but natural.
            
            Original response: "{text}"
            
            Return only the corrected version without any explanations or additional text.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # If correction fails, return original text
            return text
    
    def evaluate_star_method(self, question: str, response: str) -> dict:
        """Evaluate response using STAR method and provide feedback"""
        try:
            prompt = f"""
            Evaluate this interview response using the STAR method (Situation, Task, Action, Result).
            
            Question: "{question}"
            Response: "{response}"
            
            Analyze if the response includes:
            - Situation: Context/background
            - Task: What needed to be done
            - Action: What they specifically did
            - Result: Outcome/impact
            
            Provide a JSON response with:
            {
                "star_score": <score out of 10>,
                "missing_elements": [<list of missing STAR elements>],
                "strengths": [<what was done well>],
                "suggestions": [<specific improvements>],
                "star_analysis": {
                    "situation": <found/missing>,
                    "task": <found/missing>, 
                    "action": <found/missing>,
                    "result": <found/missing>
                }
            }
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.5
            )
            
            import json
            return json.loads(response.choices[0].message.content.strip())
            
        except Exception as e:
            return {
                "star_score": 5,
                "missing_elements": [],
                "strengths": ["Response provided"],
                "suggestions": ["Could not analyze - please try again"],
                "star_analysis": {"situation": "unknown", "task": "unknown", "action": "unknown", "result": "unknown"}
            }
    
    def generate_first_question(self, session_id: str) -> str:
        session = self.get_session(session_id)
        if not session:
            return "Session not found"
        
        company_context = f" at {session.company_name}" if session.company_name else ""
        job_context = f"for the {session.job_title} position" if session.job_title else "for this role"
        
        prompt = f"""
        You are Sarah, a friendly and experienced HR manager{company_context} conducting a live interview {job_context}.
        You are speaking directly to the candidate in person. This is what you would say out loud during the interview.
        
        Job Information:
        - Position: {session.job_title or "Not specified"}
        - Company: {session.company_name or "Not specified"}
        - Job Description: {session.job_description[:500] if session.job_description else "Not provided"}...
        
        Candidate Information:
        - Name: {session.candidate_name}
        - CV Summary: {session.cv_text[:1000]}...
        
        Provide only what you would actually say to the candidate - no names, labels, or prefixes like "Sarah:" or "Interviewer:".
        
        Start with a warm, natural greeting and ask ONE thoughtful opening question. Make it conversational and personal.
        
        Your response should:
        - Be exactly what you would say out loud (no "Sarah:" prefix)
        - Sound natural and conversational
        - Reference the specific job they're applying for
        - Show you've read their CV
        - Help assess their interest and basic fit for this role
        - Be warm but professional
        
        Just speak naturally as if you're having a live conversation. No labels, just your actual words.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250,
                temperature=0.7
            )
            
            question = response.choices[0].message.content.strip()
            session.current_question = question
            session.questions_asked.append(question)
            return question
            
        except Exception as e:
            job_ref = f" for the {session.job_title} position" if session.job_title else ""
            company_ref = f" at {session.company_name}" if session.company_name else ""
            return f"Hi {session.candidate_name}! Welcome to our interview today{company_ref}. I'm excited to learn more about you{job_ref}. Could you start by telling me what interests you most about this opportunity?"
    
    def generate_next_question(self, session_id: str, user_response: str) -> str:
        session = self.get_session(session_id)
        if not session:
            return "Session not found"
        
        # Auto-correct grammar before processing
        corrected_response = self.correct_grammar(user_response)
        session.responses.append(corrected_response)
        
        # Get STAR evaluation for the response
        if len(session.questions_asked) > 0:
            star_evaluation = self.evaluate_star_method(session.questions_asked[-1], corrected_response)
            session.star_evaluations.append(star_evaluation)
        
        # Check if interview is complete (10 questions)
        if len(session.questions_asked) >= 10:
            return "INTERVIEW_COMPLETE"
        
        conversation_history = ""
        for i, (q, r) in enumerate(zip(session.questions_asked, session.responses)):
            conversation_history += f"Q{i+1}: {q}\nA{i+1}: {r}\n\n"
        
        # Different question types based on progress
        question_number = len(session.questions_asked) + 1
        
        if question_number <= 3:
            question_type = "getting to know them, their background, and motivation for this specific role"
        elif question_number <= 6:
            question_type = f"behavioral questions relevant to {session.job_title or 'this role'} that require STAR method responses (Situation, Task, Action, Result)"
        elif question_number <= 8:
            question_type = f"technical/role-specific questions based on the {session.job_title or 'position'} requirements and their experience"
        else:
            question_type = "forward-looking questions about goals, cultural fit, and long-term alignment with this role"
        
        prompt = f"""
        You are Sarah, continuing a live interview conversation for the {session.job_title or 'open position'} role{' at ' + session.company_name if session.company_name else ''}. 
        You are speaking directly to the candidate. Provide only what you would actually say out loud.
        
        Job Context:
        - Position: {session.job_title or "Not specified"}
        - Company: {session.company_name or "Not specified"}  
        - Key Requirements: {session.job_description[:800] if session.job_description else "General role requirements"}
        
        Current focus: {question_type}
        
        Candidate: {session.candidate_name}
        CV: {session.cv_text[:600]}
        
        Previous conversation:
        {conversation_history}
        
        Based on their last response, continue the conversation naturally. Your response should:
        - Be exactly what you would say out loud (no "Sarah:" or "Interviewer:" prefix)
        - Relate to the specific job they're applying for
        - Assess skills/experience needed for this role
        - Reference their previous answers when relevant
        - For behavioral questions, ask for examples using "Tell me about a time when..." format
        - For technical questions, focus on skills mentioned in the job description
        - Show you're actively listening by commenting briefly on their response
        - Flow naturally as a real conversation
        
        Just provide your actual spoken words - no labels, no prefixes, just what you would say.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250,
                temperature=0.8
            )
            
            question = response.choices[0].message.content.strip()
            session.current_question = question
            session.questions_asked.append(question)
            return question
            
        except Exception as e:
            return f"Thank you for that response. Could you tell me more about a specific challenge you've faced in your career and how you handled it?"
    
    def generate_feedback(self, session_id: str) -> str:
        session = self.get_session(session_id)
        if not session:
            return "Session not found"
        
        conversation_summary = ""
        for i, (q, r) in enumerate(zip(session.questions_asked, session.responses)):
            conversation_summary += f"Q{i+1}: {q}\nA{i+1}: {r}\n\n"
        
        # Calculate overall STAR score
        star_scores = [eval.get('star_score', 5) for eval in session.star_evaluations if eval]
        avg_star_score = sum(star_scores) / len(star_scores) if star_scores else 5
        
        prompt = f"""
        Provide comprehensive interview feedback for this candidate applying for a specific role. You are Sarah, their interviewer, giving thoughtful and constructive feedback.
        
        Job Context:
        - Position: {session.job_title or "Not specified"}
        - Company: {session.company_name or "Not specified"}
        - Job Requirements: {session.job_description[:500] if session.job_description else "General requirements"}
        
        Candidate: {session.candidate_name}
        Interview Length: {len(session.questions_asked)} questions
        Average STAR Method Score: {avg_star_score:.1f}/10
        
        Complete Interview Conversation:
        {conversation_summary}
        
        Provide detailed feedback covering:
        
        **📊 OVERALL PERFORMANCE**
        - How well they demonstrated fit for the {session.job_title or "target"} role
        - Key strengths relevant to this position
        - Overall impression and interview performance
        
        **🎯 JOB-SPECIFIC ASSESSMENT**
        - How their background aligns with the job requirements
        - Specific skills demonstrated that match the role
        - Areas where they showed strong potential for this position
        - Any gaps between their experience and job requirements
        
        **⭐ STAR METHOD ANALYSIS**
        - How well they used the STAR method (Situation, Task, Action, Result)
        - Specific examples where STAR was used effectively
        - Areas where STAR method could be improved
        
        **💪 STRENGTHS**
        - Specific skills and qualities demonstrated
        - Communication style and interview presence
        - Examples that stood out as relevant to the role
        
        **🎯 AREAS FOR IMPROVEMENT**
        - Specific suggestions for better responses
        - Missing elements in their answers
        - How to better highlight relevant experience for this type of role
        
        **🚀 ACTION ITEMS**
        - 3-5 specific recommendations for future interviews for similar roles
        - How to better connect their experience to job requirements
        - STAR method improvements
        - Role-specific preparation suggestions
        
        **💡 FINAL THOUGHTS**
        - Assessment of their candidacy for this specific role
        - Encouragement and positive closing
        - Next steps for interview preparation
        
        Be encouraging but honest. Provide specific, actionable feedback that will help them succeed in interviews for this type of role.
        Use a warm, professional tone and reference the specific job throughout your feedback.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.6
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"""
            ## Interview Feedback for {session.candidate_name}
            
            Thank you for completing the interview! While I couldn't generate detailed AI feedback due to a technical issue, here's what I observed:
            
            **Questions Completed:** {len(session.questions_asked)}/10
            **Responses Provided:** {len(session.responses)}
            
            **General Recommendations:**
            - Practice using the STAR method (Situation, Task, Action, Result) for behavioral questions
            - Prepare specific examples from your experience
            - Work on providing concrete results and outcomes
            
            Keep practicing, and you'll continue to improve!
            """

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