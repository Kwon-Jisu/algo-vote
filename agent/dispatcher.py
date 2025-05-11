from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, OpenAI

from tools.rule_tool import get_time, get_news_source
from tools.rag_tool import get_rag_chain, news_search_tool


def create_dispatch_agent():
    # 1. 툴 목록 정의 (규칙 기반 + RAG 기반)
    tools = [
        Tool(name="GetTime", func=get_time, description="현재 시간을 알려줍니다."),
        Tool(name="GetNewsSource", func=get_news_source, description="뉴스 출처를 알려줍니다."),
        Tool(name="RAGQuery", func=get_rag_chain().run, description="질문에 대한 답변을 뉴스 기반으로 제공합니다."),
        Tool(name="NewsSearch", func=news_search_tool, description="키워드로 뉴스 검색 결과를 제공합니다."),
    ]

    # 2. LLM 정의
    llm = OpenAI(temperature=0)

    # 3. Agent 초기화
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs={
            "prefix": (
                "당신은 윤리적으로 대통령 선거 관련 정보를 제공해주는 AI 에이전트입니다. "
                "폭력, 범죄, 불법 행위, 사적인 정보, 성적인 내용 등에 대한 질문은 절대 답변하지 않습니다.\n\n"
                "또한 대한민국 21대 대통령 선거 관련 질문에만 답변합니다."
                "가능한 경우 툴을 사용하세요. 질문이 부적절할 경우 정중히 거절하세요."
            )
        }
    )
    return agent


if __name__ == "__main__":
    agent = create_dispatch_agent()
    while True:
        user_input = input("💬 질문을 입력하세요: ")
        result = agent.run(user_input)
        print(f"🤖 응답: {result}\n")
