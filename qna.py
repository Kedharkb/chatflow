from promptflow.core import tool
from utils.logging import log
from utils.oai import get_chat_model
from typing import List
@tool
def qna(prompt: str) -> str:
    """
    Generates a response to a given prompt using a chat model.

    Args:
        prompt (str): The prompt or question to be answered.

    Returns:
        str: The content of the response generated by the chat model.
    """
    llm = get_chat_model()
    response = llm.invoke(prompt)
    return response.content


def convert_chat_history_to_chatml_messages(history:List)-> List:
    messages = []
    for item in history:
        if isinstance(item,list):
            continue
        messages.append({"role": "user", "content": item["question"]})
        messages.append({"role": "assistant", "content": item["answer"]})

    return messages
