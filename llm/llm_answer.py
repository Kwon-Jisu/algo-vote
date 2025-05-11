import os

from supabase import create_client, Client
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.runnables import RunnableLambda

from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI(title="RAG Chatbot")

supabase_url = "https://jajjrmucygccmtxxsvhd.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImphampybXVjeWdjY210eHhzdmhkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY0MzUwNDMsImV4cCI6MjA2MjAxMTA0M30.7eSk0U7JcS344aA_XARElDfJ0wSl8GcOJQUmHWRcV6Q"
supabase = create_client(supabase_url, supabase_key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyC0m3f4yJ9zTESEtCgOdwcrvhg1YxPWYdk"

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")
vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="information",
    query_name="match_documents"
)
retriever = vector_store.as_retriever()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", thinking_budget=1024)

# 프롬프트 템플릿
qa_prompt = PromptTemplate.from_template(
    """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Answer in Korean.

# Context:
{context}

# Question:
{question}

# Answer:"""
)

rewrite_prompt = PromptTemplate.from_template(
    """You are an assistant that rewrites user questions to include relevant context.
Use the conversation history and the user's new question to generate a “contextualized question.”
Answer in Korean.

# Conversation History:
{history}

# New Question:
{question}

# Contextualized Question:"""
)


class ControlledConversationBufferMemory(ConversationBufferMemory):
    def save_context(self, *args, **kwargs):
        pass  # 자동 저장을 비활성화합니다

    def write_context(self, inputs: dict, outputs: dict):
        super().save_context(inputs, outputs)


# 메모리 인스턴스 생성
memory = ControlledConversationBufferMemory(
    memory_key="history",
    return_messages=False
)

qa_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | qa_prompt
        | llm
        | StrOutputParser()
)

rewrite_chain = LLMChain(
    llm=llm,
    prompt=rewrite_prompt,
    memory=memory,
    output_parser=StrOutputParser(output_key="answer")
)


def ask_question(question: str) -> str:
    """
    주어진 질문에 대해 저장된 컨텍스트를 활용하여 답변을 반환합니다.
    """
    answer = qa_chain.invoke(question)
    memory.write_context({"human": question}, {"ai": answer})
    return answer


def ask_followup_question(question: str) -> str:
    """
    후속 질문을 컨텍스트와 대화 이력을 반영하여 재작성한 뒤 답변을 반환합니다.
    """
    contextualized = rewrite_chain.run(question=question)
    answer = qa_chain.invoke(contextualized)
    memory.write_context({"human": question}, {"ai": answer})
    return answer


def chatbot(question):
    if memory.buffer == "":
        return ask_question(question)
    else:
        return ask_followup_question(question)


# --- 요청/응답 스키마 ---
class PredictRequest(BaseModel):
    question: str


class PredictResponse(BaseModel):
    answer: str


# --- 엔드포인트 정의 ---
@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    사용자 질문을 받아 RAG 기반 챗봇 응답을 반환합니다.
    """
    answer = chatbot(request.question)
    return PredictResponse(answer=answer)


@app.get("/health")
async def health():
    return {"status": "ok"}