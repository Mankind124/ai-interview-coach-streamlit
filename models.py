from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class InterviewSession:
    session_id: str
    candidate_name: Optional[str] = None
    cv_text: Optional[str] = None
    job_title: Optional[str] = None
    job_description: Optional[str] = None
    company_name: Optional[str] = None
    current_question: Optional[str] = None
    questions_asked: List[str] = None
    responses: List[str] = None
    star_evaluations: List[Dict] = None
    corrected_responses: List[str] = None
    is_active: bool = True
    
    def __post_init__(self):
        if self.questions_asked is None:
            self.questions_asked = []
        if self.responses is None:
            self.responses = []
        if self.star_evaluations is None:
            self.star_evaluations = []
        if self.corrected_responses is None:
            self.corrected_responses = []