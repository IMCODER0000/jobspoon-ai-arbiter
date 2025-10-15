from typing import List, Dict, Optional

from pydantic import BaseModel

from interview.service.request.question_generate_endInterview_request import EndInterviewRequest



class QuestionGenerationEndInterviewRequestForm(BaseModel):
    userToken: str
    interviewId: int
    questionId: List[int]
    context: Dict[str, str]
    questions: List[str]
    answers: List[str]
    callbackUrl: Optional[str] = None

    def toEndInterviewRequest(self):
        return EndInterviewRequest(
            userToken=self.userToken,
            interviewId=self.interviewId,
            questionId=self.questionId,
            context=self.context,
            questions=self.questions,
            answers=self.answers,
            callbackUrl=self.callbackUrl
        )
