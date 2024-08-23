__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from promptflow.core import tool
import os
from utils.logging import log
from utils.index import ChromaDBClient
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from utils.oai import get_openai_embedding
from constants import DOCUMENTS_PATH

@tool
def build_index_tool(pdf_path: str,collection_name='signals_system') -> str:
    """
    This function builds an index from a PDF document and stores it in a ChromaDB collection.
    Arguments:
    - pdf_path: The file path to the PDF document to be indexed.
    - collection_name: The name of the ChromaDB collection where the index will be stored.
                       Defaults to 'signals_system'.
    Returns:
    - The name of the collection where the index was built.
    """
        
    chunk_size = int(os.environ.get("CHUNK_SIZE"))
    chunk_overlap = int(os.environ.get("CHUNK_OVERLAP"))
    log(f"Chunk size: {chunk_size}, chunk overlap: {chunk_overlap}")
    
    embeddings = get_openai_embedding()    
    chroma_client = ChromaDBClient(path=DOCUMENTS_PATH,collection_name=collection_name,embedding=embeddings)
    collection = chroma_client.get_collection()

    loader = PyPDFLoader(pdf_path)
    document = loader.load()
    
    # Check if the collection does not exist (i.e., it's None or empty)
    if not collection:
        # Split the document into chunks using the RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        segments = text_splitter.split_documents(document)
        
        chroma_client.create_collection()
        
        # Save the split document segments to the collection
        chroma_client.save_documents(documents=segments)
    else:
        log(f'{collection} already exists and skipping index building.')

    return collection_name


    
