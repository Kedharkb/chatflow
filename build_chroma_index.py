__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from promptflow.core import tool
import os
from utils.logging import log
from utils.index import ChromaDBClient
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings

@tool
def build_index_tool(pdf_path: str,collection_name='signals_system') -> str:
    chunk_size = int(os.environ.get("CHUNK_SIZE"))
    chunk_overlap = int(os.environ.get("CHUNK_OVERLAP"))
    log(f"Chunk size: {chunk_size}, chunk overlap: {chunk_overlap}")
    embdeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"),model = os.environ.get("EMBEDDING_MODEL_DEPLOYMENT_NAME"))    
    chroma_client = ChromaDBClient(path='./documents/',collection_name=collection_name,embedding=embdeddings)
    loader = PyPDFLoader(pdf_path)
    document = loader.load()
    collection = chroma_client.get_collection()
    if not collection:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        segments = text_splitter.split_documents(document)
        chroma_client.create_collection()
        chroma_client.save_documents(documents=segments)
    else:
        log(f'{collection} already exists and skipping index building.')

    return collection_name


    
