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
from utils.oai import get_openai_embedding
from constants import DOCUMENTS_PATH

@tool
def build_faiss_index(pdf_path: str,faiss_index_name='signals_system') -> str:
    """
    This function builds a FAISS index from a PDF document and stores it in a specified collection.
    Arguments:
    - pdf_path: The file path to the PDF document to be indexed.
    - collection_name: The name of the collection where the index will be stored.
                       Defaults to 'signals_system'.
    Returns:
    - The name of the collection where the index was built.
    """

    chunk_size = int(os.environ.get("CHUNK_SIZE"))
    chunk_overlap = int(os.environ.get("CHUNK_OVERLAP"))
    log(f"Chunk size: {chunk_size}, chunk overlap: {chunk_overlap}")
    
    # Load the PDF document using the PyPDFLoader
    loader = PyPDFLoader(pdf_path)
    document = loader.load()
    
    embeddings = get_openai_embedding()       
    faiss_index =  FAISSIndex(index=faiss.IndexFlatL2(1536), embedding=embeddings,index_name=faiss_index_name,documents_path=DOCUMENTS_PATH)
    
    # Check if the FAISS index already exists
    is_exists = faiss_index.index_exists()
    if not is_exists:
         # Split the document into chunks using the RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        segments = text_splitter.split_documents(document)

        # Save the split document segments to the FAISS index
        faiss_index.save_documents(documents=segments)
    else:
        log(f'vector_store already exists and skipping index building.')

    return faiss_index_name
