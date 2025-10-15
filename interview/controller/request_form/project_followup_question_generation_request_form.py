from typing import List, Optional
from pydantic import BaseModel

from interview.entity.job_category import JobCategory
from interview.entity.project_experience import ProjectExperience
from interview.entity.interview_tech_stack import InterviewTechStack
from interview.service.request.project_followup_generation_request import ProjectFollowupGenerationRequest



class FastApiAccountProjectRequest(BaseModel):
    projectName: str
    projectDescription: str


class ProjectFollowupQuestionGenerationRequestForm(BaseModel):
    userToken: str
    interviewId: int
    topic: int
    techStack: list[str]  # 문자열 리스트로 변경 (Java에서 문자열로 보냄)
    projectExperience: int
    companyName: str
    questionId: int
    answerText: str
    projectResponses: Optional[List[FastApiAccountProjectRequest]] = None  # 프로젝트 리스트 (null 허용)

    def toProjectFollowupQuestionRequest(self):
        job_name = JobCategory.get_job_name(self.topic)
        project_experience = ProjectExperience.get_project_experience(self.projectExperience)
        # techStack은 이미 문자열 리스트이므로 그대로 사용
        tech_stack = self.techStack

        # 모든 프로젝트의 이름과 설명을 결합
        if self.projectResponses and len(self.projectResponses) > 0:
            project_descriptions = []
            for idx, project in enumerate(self.projectResponses, 1):
                project_descriptions.append(
                    f"{idx}. {project.projectName} 프로젝트: {project.projectDescription}"
                )
            project_description = "\n".join(project_descriptions)
        else:
            # 프로젝트가 없을 경우 명확한 메시지
            project_description = "지원자가 등록한 프로젝트가 없습니다. 일반적인 프로젝트 경험에 대한 질문을 생성해주세요."

        return ProjectFollowupGenerationRequest(
            interviewId=self.interviewId,
            topic=job_name,
            techStack=tech_stack,
            projectExperience=project_experience,
            projectDescription=project_description,
            companyName=self.companyName,
            questionId=self.questionId,
            answerText=self.answerText,
            userToken=self.userToken,
        )