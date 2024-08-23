__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from promptflow import tool
import os
from utils.index import ChromaDBClient, FAISSIndex
from utils.oai import render_chat_template_with_token_limit, get_openai_embedding
from utils.logging import log
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
import faiss
from constants import DOCUMENTS_PATH
from templates.system_messages import system_message1, system_message2

def get_documents(question:str,is_chroma:bool, collection_name:str):
    """
    Retrieves documents relevant to the question from either a ChromaDB or FAISS index.

    Args:
        question (str): The question to retrieve documents for.
        is_chroma (bool): Whether to use ChromaDB (True) or FAISS index (False).
        collection_name (str): The name of the ChromaDB collection or FAISS index.

    Returns:
        list: A list of relevant documents retrieved from the specified database.
    """
        
    embeddings = get_openai_embedding()    
    if is_chroma:
        chroma_client = ChromaDBClient(path=DOCUMENTS_PATH,collection_name=collection_name, embedding=embeddings)
        results = chroma_client.query(query_text=question)
    else:
        faiss_index =  FAISSIndex(index=faiss.IndexFlatL2(1536), embedding=embeddings,index_name=collection_name,documents_path=DOCUMENTS_PATH)
        results = faiss_index.query(text=question)
    return results


@tool
def retrieval(question: str, history: list,chroma_collection_name: str=None,faiss_index_name:str=None,use_history:bool=False) -> str:
    """
    Retrieves relevant documents and constructs a chat prompt based on the question and conversation history.

    Args:
        question (str): The question to be answered.
        history (list): The conversation history to use for context, if applicable.
        chroma_collection_name (str, optional): The name of the ChromaDB collection. Defaults to None.
        faiss_index_name (str, optional): The name of the FAISS index. Defaults to None.
        use_history (bool, optional): Whether to include conversation history in the prompt. Defaults to False.

    Returns:
        str: The constructed prompt that includes the relevant documents and question.
    """

    is_chroma_collection = True if chroma_collection_name else False
    collection_name= chroma_collection_name if chroma_collection_name else faiss_index_name
    log(f"collection name {chroma_collection_name}, {faiss_index_name}")
    
    # Retrieve relevant documents based on the question.
    results = get_documents(question,is_chroma_collection,collection_name)
    documents = [doc.page_content for doc in results]
    token_limit = int(os.environ.get("PROMPT_TOKEN_LIMIT"))
    
    # Define the template messages.
    context_message = "Context:\n{context}"
    question_message = "Question:\n{question}"
   
    messages = [
    ("system", system_message1),
    ("system", system_message2)]   
    
    chat_history = []
    if use_history:
        # Include chat history in the prompt if use_history is True.
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
    """
    Converts a list of conversation history items into ChatML messages.

    Args:
        history (list): The conversation history to convert.

    Returns:
        list: A list of ChatML messages constructed from the history.
    """
    history_messages = ChatMessageHistory()
    for item in history:
        if isinstance(item,list):
            continue
        # Add user and AI messages to the chat history.
        history_messages.add_user_message(item["question"])
        history_messages.add_ai_message(item["answer"])

    return history_messages.messages