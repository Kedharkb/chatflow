import os
from typing import  List,Any
from faiss import Index
import chromadb
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction
from langchain.vectorstores import Chroma, FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from utils.logging import log

class FAISSIndex:
    def __init__(self, index: Index, embedding: Any,index_name:str,documents_path:str) -> None:
        self.index = index
        self.embedding = embedding
        self.index_name = index_name
        self.documents_path = documents_path


    def query(self, text: str, top_k: int = 10) -> List:
        vector_store = self.load_vectorstore()
        docs = vector_store.similarity_search(query=text,k=top_k)
        log(f'docs,{docs}')
        return docs

    def save_documents(self, documents:List) -> None:
        vector_store = FAISS(
            embedding_function=self.embedding,
            index=self.index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        vector_store.add_documents(documents=documents)
        vector_store.save_local(folder_path=self.documents_path,index_name=self.index_name)
    
    def load_vectorstore(self):
        vector_store=FAISS.load_local(folder_path=self.documents_path,index_name=self.index_name,embeddings=self.embedding, allow_dangerous_deserialization=True)
        return vector_store
    
    def index_exists(self):
        # Check if the index directory exists
        return os.path.exists(f'{self.documents_path}/{self.index_name}.faiss')



class ChromaDBClient:
    def __init__(self,path:str, collection_name:str, embedding: Any) -> None:
        self.chroma_client = chromadb.PersistentClient(path=path)
        self.collection_name = collection_name
        self.embedding = embedding    
    
    def create_collection(self,):
        return self.chroma_client.create_collection(name=self.collection_name)
    
    def save_documents(self, documents:List):
        langchain_chroma = Chroma(
        client=self.chroma_client,
        collection_name=self.collection_name,
        embedding_function=self.embedding,
    )
        langchain_chroma.add_documents(documents)

    def query(self,query_text:str):
        db = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embedding,
                                )
        docs = db.similarity_search(query_text,k=10)
        return docs
    
    def get_collection(self):
        try:
            embedding_function = OpenAIEmbeddingFunction(api_key=os.environ.get("OPENAI_API_KEY"),model_name=os.environ.get("EMBEDDING_MODEL_DEPLOYMENT_NAME"))
            collection= self.chroma_client.get_collection(name=self.collection_name,embedding_function=embedding_function)
            return collection
        except Exception as e:
            return None

              

        