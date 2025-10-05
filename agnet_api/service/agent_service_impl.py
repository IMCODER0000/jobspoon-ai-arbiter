import os
from dotenv import load_dotenv
from langchain_community.utils.math import cosine_similarity
from langchain_openai import ChatOpenAI
from agnet_api.entity.embedding import get_embedding
from agnet_api.repository.agent_repository_impl import AgentRepositoryImpl
from agnet_api.repository.rag_repository_impl import RagRepositoryImpl
from agnet_api.repository.simiarity_repository_impl import SimilarityRepositoryImpl
from agnet_api.repository.tech_repository_impl import TechRepositoryImpl

load_dotenv()

class AgentServiceImpl:
    def __init__(self):
        self.agentRepository = AgentRepositoryImpl()
        self.ragRepository = RagRepositoryImpl()
        self.similarityRepository = SimilarityRepositoryImpl()
        self.techRepository = TechRepositoryImpl()
        self.openAPI = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

    async def get_best_followup_question(self, companyName: str, topic: str, situation: str, gpt_question: str, userToken:str):
        # situation : answerText (이전 질문에 대한 면접자의 답변)
        print(f" AGENT started: company={companyName}, topic={topic}, userToken={userToken}")

        # GPT 질문 VS answerText 유사도 비교 ->  결과: score
        #print(f" type(situation): {type(situation)}, type(gpt_question): {type(gpt_question)}")
        score_of_gpt = self.similarityRepository.embeddingForGPT(situation, gpt_question, userToken)

        # RAG 1차 (메인 회사 DB 조회)
        rag_main_result = self.ragRepository.rag_main(companyName, situation, userToken)
        #print(f" AGENT 도메인의 RAG Main 결과: {rag_main_result}")
        #print("🧪 main_rag_result type:", type(rag_main_result))

        # RAG 1차 유사도 점수, 유사도가 제일 높은 질문 1개
        main_rag_score, main_rag_question = self.similarityRepository.embeddingForMainRAG(situation, rag_main_result, userToken)


        # RAG 2차 (Fallback DB) 조건부 호출
        rag_fallback_result = []
        if rag_main_result == ["(메인 회사 DB에서 적절한 질문을 찾지 못했습니다.)"]:
            print(f" RAG Main 실패 → Fallback DB 조회 진행")
            rag_fallback_result = self.ragRepository.rag_fallback(situation, userToken)
            print(f" RAG Fallback 결과: {rag_fallback_result}")
        # RAG 2차 (Fallback DB) 유사도 계산
        fallback_rag_score, fallback_rag_question = self.similarityRepository.embeddingForFallbackRAG(situation, rag_fallback_result, userToken)


        # 3. AGENT에게 최종 선택 요청   decision_prompt
        final_question= self.agentRepository.build_decision_prompt(
            #companyName, topic, situation, gpt_question, rag_main_result, rag_fallback_result
            score_of_gpt, gpt_question, main_rag_score, main_rag_question, fallback_rag_score, fallback_rag_question, userToken
        )
        print(f"최종 질문: {final_question}")
        #print(f"📝 AGENT Prompt:\n{decision_prompt}")

        #response = self.openAPI.invoke(decision_prompt)
        #print(f"AGENT 최종 선택: {response}")

        # response가 AIMessage 객체라면 content를 꺼내야 함
        #final_question = response.content if hasattr(response, "content") else str(response)

        # used_context / summary 리턴 포맷
        #used_context = "\n".join(rag_main_result or rag_fallback_result)
        #summary = f"{companyName} DB 검색 + Fallback 여부 포함"

        return final_question


    async def get_best_tech_question(self, techStack: list[str], situation: str, userToken: str):
        print(f"AGENT tech started: userToken={userToken}")

        # tech DB에 참고하기 : techStack기술중 DB에 있는거면 참고하고, 없는거면 참고 안하고.
        rag_tech_result = self.ragRepository.rag_tech(techStack, situation, userToken)
        #print(f" AGENT 도메인의 RAG Tech 결과: {rag_tech_result}")

        # 임베딩하고, 점수매기는거 여기서하셈
        top_tech_questions = self.techRepository.embeddingForTech(rag_tech_result, situation, userToken)
        #print(f"{top_tech_questions}")

        return top_tech_questions
        #final_question = await self.techRepository.generateTechFollowupQuestion()