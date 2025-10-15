from pydantic import BaseModel


class ProjectFollowupGenerationRequest(BaseModel):
    interviewId: int
    topic: str
    techStack: list[str]
    projectExperience: str
    projectDescription: str  # 프로젝트 설명 추가
    companyName: str
    questionId: int
    answerText: str
    userToken: str





