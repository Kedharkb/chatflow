from promptflow.core import tool
import os
from utils.logging import log
from langchain_openai import ChatOpenAI
@tool
def qna(prompt: str):
    max_completion_tokens = int(os.environ.get("MAX_COMPLETION_TOKENS"))
    llm = ChatOpenAI(model=os.environ.get("CHAT_MODEL_DEPLOYMENT_NAME"),max_tokens=max_completion_tokens)
    response = llm.invoke(prompt)
    return response.content


def convert_chat_history_to_chatml_messages(history):
    messages = []
    for item in history:
        if isinstance(item,list):
            continue
        messages.append({"role": "user", "content": item["question"]})
        messages.append({"role": "assistant", "content": item["answer"]})

    return messages
