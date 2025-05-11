from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain.tools import tool

from crawler.debates_crawler import search_news

# .env 파일 로드
load_dotenv()


def get_rag_chain() -> RetrievalQA:
    # 환경변수에서 API 키 가져오기
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")

    # FAISS 인덱스 로딩 (임베딩은 OpenAI 기준. 변경 가능)
    vectorstore = FAISS.load_local("vector_store/faiss_index", OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()

    # Gemini LLM 초기화 (temperature 조정 가능)
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )


@tool
def news_search_tool(query: str) -> str:
    """키워드로 뉴스 검색 결과를 반환합니다."""
    results = search_news(query)
    return "\n".join(results)


# from google import genai
#
# client = genai.Client(api_key="AIzaSyCm86zvHc84q6MH9ERQwNZUTmngOvZLzho")
#
# response = client.models.generate_content(
#                 model="gemini-2.5-flash-preview-04-17",
#                 contents=[image, prompt.format(question, real_answer).strip()]
#             )
# result=response.text.strip()
# # response = client.models.generate_content(
#                 model="gemini-2.5-flash-preview-04-17",
#                 contents=prompt.format(question, real_answer).strip()
#             )
# # result=response.text.strip()
