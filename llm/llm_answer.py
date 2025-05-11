from dotenv import load_dotenv
import os

from supabase import create_client, Client
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.runnables import RunnableLambda

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI(title="RAG Chatbot")

# .env 파일 로드
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(supabase_url, supabase_key)
google_api_key = os.getenv("GOOGLE_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")
# embeddings = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-small')

# 문서 불러오기 (.txt 파일)
loader = TextLoader("../preprocess/2025.05.02.txt", encoding="utf-8")
documents = loader.load()  # LangChain Document 객체 리스트

# Splitter 정의 및 실행
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

vector_store = SupabaseVectorStore.from_documents(
    docs,
    embeddings,
    client=supabase,
    table_name="debate_information"
)
