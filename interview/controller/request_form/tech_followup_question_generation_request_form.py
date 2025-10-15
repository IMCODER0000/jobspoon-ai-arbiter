from openai import BaseModel

from interview.service.request.tech_followup_generation_request import TechFollowupGenerationRequest



class TechFollowupQuestionGenerationRequestForm(BaseModel):
    interviewId: int
    techStack: list[str]  # 문자열 리스트로 변경 (Java에서 문자열로 보냄)
    questionId: int
    answerText: str
    userToken: str

    def toTechFollowupQuestionRequest(self):
        # techStack은 이미 문자열 리스트이므로 그대로 사용
        tech_stack = self.techStack

        return TechFollowupGenerationRequest(
            interviewId=self.interviewId,
            techStack=tech_stack,
            questionId=self.questionId,
            answerText=self.answerText,
            userToken=self.userToken,
        )
