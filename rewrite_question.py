from jinja2 import Environment, FileSystemLoader
import os
from utils.logging import log
from utils.oai import  render_jinja_template_with_token_limit
from promptflow import tool
from langchain_openai import ChatOpenAI

@tool
def rewrite_question(question: str, history: list):
    template = Environment(
        loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__)))
    ).get_template("rewrite_question_prompt.md")
    token_limit = int(os.environ.get("PROMPT_TOKEN_LIMIT"))

    max_completion_tokens = int(os.environ["MAX_COMPLETION_TOKENS"])
    chat_model = ChatOpenAI(model_name=os.environ.get("CHAT_MODEL_DEPLOYMENT_NAME"),max_tokens=max_completion_tokens)

    while True:
        try:
            prompt = render_jinja_template_with_token_limit(
                template, token_limit, question=question, history=history
            )
            break
        except ValueError:
            history = history[:-1]
            log(f"Reducing chat history count to {len(history)} to fit token limit")
    
    rewritten_question = chat_model.invoke([ ("human", prompt)])
    log(f"Rewritten question: {rewritten_question}")

    return rewritten_question.content
