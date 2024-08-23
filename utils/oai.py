import tiktoken
from jinja2 import Template
from .logging import log
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
import os
from jinja2 import Environment, FileSystemLoader

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates/'))


def count_token(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def load_template(template_name:str):
    template = Environment(
        loader=FileSystemLoader(template_dir)
    ).get_template(template_name)
    
    return template

def render_chat_template_with_token_limit(template: ChatPromptTemplate, token_limit: int, question, context, history:list) -> str:
    context_text = "\n".join([f"## Context #{i+1}\n{c}" for i, c in enumerate(context)])
    text = template.format(
    context=context_text,
    question=question,
    chat_history=[]
    )   
    messages = template.format_messages(chat_history=history,context=context_text,question=question)
    token_count = count_token(text)
    if token_count > token_limit:
        message = f"token count {token_count} exceeds limit {token_limit}"
        raise ValueError(message)
    return messages

def render_jinja_template_with_token_limit(template: Template, token_limit: int, **kwargs) -> str:
    text = template.render(**kwargs)
    token_count = count_token(text)
    if token_count > token_limit:
        message = f"token count {token_count} exceeds limit {token_limit}"
        log(message)
        raise ValueError(message)
    return text

def get_openai_embedding():
    return OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"),model = os.environ.get("EMBEDDING_MODEL_DEPLOYMENT_NAME"))

def get_chat_model():
     return ChatOpenAI(model_name=os.environ.get("CHAT_MODEL_DEPLOYMENT_NAME"),max_tokens=int(os.environ["MAX_COMPLETION_TOKENS"]))



if __name__ == "__main__":
    print(count_token("hello world, this is impressive"))
