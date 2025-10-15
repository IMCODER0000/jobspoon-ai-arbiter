from typing import List, Optional
from pydantic import BaseModel

from interview.entity.project_experience import ProjectExperience
from interview.service.request.project_question_generation_request import ProjectQuestionGenerationRequest


class FastApiAccountProjectRequest(BaseModel):
    projectName: str
    projectDescription: str


class ProjectQuestionGenerationRequestForm(BaseModel):
    userToken: str
    interviewId: int
    projectExperience: int  # 프로젝트 경험
    questionId: int
    projectResponses: Optional[List[FastApiAccountProjectRequest]] = None  # 프로젝트 리스트 (null 허용)


    def toProjectQuestionGenerationRequest(self):
        project_experience = ProjectExperience.get_project_experience(self.projectExperience)

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

        return ProjectQuestionGenerationRequest(
            interviewId=self.interviewId,
            projectExperience=project_experience,
            userToken=self.userToken,
            questionId=self.questionId,
            projectDescription=project_description,
        )
