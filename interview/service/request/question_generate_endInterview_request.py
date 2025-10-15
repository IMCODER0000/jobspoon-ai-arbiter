from pydantic import BaseModel
from typing import List, Dict, Optional

class EndInterviewRequest(BaseModel):
    userToken: str
    interviewId: int
    questionId: List[int]
    context: Dict[str, str]
    questions: List[str]
    answers: List[str]
    callbackUrl: Optional[str] = None