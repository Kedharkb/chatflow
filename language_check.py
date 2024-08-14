
from promptflow import tool
from lingua import Language, LanguageDetectorBuilder
from utils.logging import log

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def language_check_tool(question: str) -> str:
    languages = [Language.ENGLISH, Language.GERMAN]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()
    language = detector.detect_language_of(question)
    log(f"language,{language}")
    try:
        return language == Language.ENGLISH or  language == Language.GERMAN
    except:
        return False
