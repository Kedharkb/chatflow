__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from promptflow import tool
from utils.logging import log
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.index import FAISSIndex
import faiss
from langchain_openai import OpenAIEmbeddings

@tool
def build_faiss_index(pdf_path: str,collection_name='signals_system') -> str:
    chunk_size = int(os.environ.get("CHUNK_SIZE"))
    chunk_overlap = int(os.environ.get("CHUNK_OVERLAP"))
    log(f"Chunk size: {chunk_size}, chunk overlap: {chunk_overlap}")

    loader = PyPDFLoader(pdf_path)
    document = loader.load()
    embeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"),model = os.environ.get("EMBEDDING_MODEL_DEPLOYMENT_NAME"))     
    faiss_index =  FAISSIndex(index=faiss.IndexFlatL2(1536), embedding=embeddings,index_name=collection_name)
    is_exists = faiss_index.index_exists()
    if not is_exists:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        segments = text_splitter.split_documents(document)
        faiss_index.save_documents(documents=segments)
    else:
        log(f'vector_store already exists and skipping index building.')

    return collection_name
