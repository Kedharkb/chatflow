from promptflow import tool
from utils.logging import log
from utils.oai import  get_chat_model, load_template


@tool
def generate_result_tool(question1:str,result1: str,question2:str, result2:str,language_check:bool) -> str:
    """
    Generates a result by comparing two question-response pairs and selects the most appropriate response.
    
    Args:
        question1 (str): The first question to consider.
        result1 (str): The response corresponding to the first question.
        question2 (str): The second question to consider.
        result2 (str): The response corresponding to the second question.
        language_check (bool): A flag indicating whether the language check passed (True) or failed (False).
    
    Returns:
        str: The most appropriate response based on the comparison or a polite message if the language check fails.
    """
        
    polite_message = (
        "Thank you for your input. For a better experience, please ask questions in English or German only."
    )

    if not language_check:
        return polite_message
    
    template = load_template("response_filter_prompt.md")
    chat_model = get_chat_model()
    
    text = template.render(question1=question1,question2=question2,response1=result1,response2=result2)
    response = chat_model.invoke([ ("human", text)])
    return result1 if response.content == 'Response1' else result2

    
    
