__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from promptflow import tool
import os
from utils.index import ChromaDBClient, FAISSIndex
from utils.oai import render_chat_template_with_token_limit
from utils.logging import log
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
import faiss
from langchain_openai import OpenAIEmbeddings


def get_documents(question:str,is_chroma:bool, collection_name:str):
    embeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"),model = os.environ.get("EMBEDDING_MODEL_DEPLOYMENT_NAME"))     
    if is_chroma:
        chroma_client = ChromaDBClient(path='./documents/',collection_name=collection_name, embedding=embeddings)
        results = chroma_client.query(query_text=question)
    else:
        faiss_index =  FAISSIndex(index=faiss.IndexFlatL2(1536), embedding=embeddings,index_name=collection_name)
        results = faiss_index.query(text=question)
    return results


@tool
def retrieval(question: str, history: list,chroma_collection_name: str=None,faiss_index_name:str=None,use_history:bool=False) -> str:
    is_chroma_collection = True if chroma_collection_name else False
    collection_name= chroma_collection_name if chroma_collection_name else faiss_index_name
    log(f"collection name {chroma_collection_name}, {faiss_index_name}")

    results = get_documents(question,is_chroma_collection,collection_name)
    documents = [doc.page_content for doc in results]
    token_limit = int(os.environ.get("PROMPT_TOKEN_LIMIT"))
    
    system_message1= "You are a smart assistant who answers questions based on the provided context and previous conversation history."
    system_message_2 ="Use the context to answer the question at the end, noting that the context has order and importance. Context #1 is more important than #2. Try as much as you can to answer based on the provided context. If you cannot derive the answer from the context, say 'I don't know.' Answer in the same language as the question."
    context_message = "Context:\n{context}"
    question_message = "Question:\n{question}"
    messages = [
    ("system", system_message1),
    ("system", system_message_2)]   
    
    chat_history = []
    if use_history:
        messages.append(MessagesPlaceholder(variable_name="chat_history"))
        chat_history= convert_chat_history_to_chatml_messages(history)
    
    messages.extend([
    ("system", context_message),
    ("human", question_message)
    ])
    
    chat_prompt_template = ChatPromptTemplate(messages)
    
    # Try to render the template with token limit and reduce snippet count if it fails
    while True:
        try:
            prompt = render_chat_template_with_token_limit(
                chat_prompt_template, token_limit, question=question, context=documents,history=chat_history)
            log(prompt)
            break

        except ValueError:
            documents = documents[:-1]
            log(f"Reducing snippet count to {len(documents)} to fit token limit")

    return {"prompt": prompt}



def convert_chat_history_to_chatml_messages(history):
    history_messages = ChatMessageHistory()
    for item in history:
        if isinstance(item,list):
            continue
        history_messages.add_user_message(item["question"])
        history_messages.add_ai_message(item["answer"])

    return history_messages.messages