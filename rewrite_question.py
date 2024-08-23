from jinja2 import Environment, FileSystemLoader
import os
from utils.logging import log
from utils.oai import  render_jinja_template_with_token_limit, get_chat_model, load_template
from promptflow import tool
import json


@tool
def rewrite_question(question: str, history: list):
    template = load_template("rewrite_question_prompt.md")
    
    token_limit = int(os.environ.get("PROMPT_TOKEN_LIMIT"))

    chat_model = get_chat_model()

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
    data = json.loads(rewritten_question.content)
    question1 = data.get('question1')
    question2 = data.get('question2')    
    return {'rewritten_question1':question1,'rewritten_question2':question2}
