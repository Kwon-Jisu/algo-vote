import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from dotenv import load_dotenv

# 환경변수 로딩
load_dotenv()

# 예시 문서 리스트 (문자열 기반)
texts = [
    "FAISS는 Facebook AI에서 개발한 벡터 검색 라이브러리입니다.",
    "RAG는 Retrieval-Augmented Generation의 약자로, 외부 문서를 검색해 답변을 생성합니다.",
    "LangChain은 LLM 기반 애플리케이션을 쉽게 만들 수 있도록 도와주는 프레임워크입니다."
]

# 문서 객체 리스트 생성
documents = [Document(page_content=text) for text in texts]

# 임베딩 모델 설정 (OpenAI 사용)
embedding_model = OpenAIEmbeddings()

# 문서 벡터화 및 FAISS 인덱스 생성
vectorstore = FAISS.from_documents(documents, embedding_model)

# 디스크에 저장
vectorstore.save_local("vector_store/faiss_index")

print("FAISS 벡터스토어가 저장되었습니다.")
