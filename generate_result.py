
from promptflow import tool
from utils.logging import log

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def generate_result_tool(llm_result: str,language_fail:bool) -> str:
    polite_message = (
        "Thank you for your input. For a better experience, please ask questions in English only."
    )


    if not language_fail:
        return polite_message
    return llm_result
