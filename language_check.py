from promptflow import tool
from lingua import Language, LanguageDetectorBuilder

@tool
def language_check_tool(question: str) -> bool:
    """
    This function checks whether the language of a given text (question) is among the allowed languages.
    Arguments:
    - question: The text whose language needs to be checked.
    Returns:
    - True if the language is among the allowed languages (English or German), False otherwise.
    """

    allowed_languages = [Language.ENGLISH, Language.GERMAN]
    
    languages = [
        Language.ENGLISH, Language.GERMAN, Language.FRENCH, Language.SPANISH,
        Language.ITALIAN, Language.DUTCH, Language.PORTUGUESE, Language.RUSSIAN,
        Language.SWEDISH, Language.DANISH, Language.NYNORSK, Language.FINNISH,
        Language.GREEK, Language.POLISH, Language.CZECH, Language.SLOVAK,
        Language.HUNGARIAN, Language.ROMANIAN, Language.BULGARIAN, Language.CROATIAN,
        Language.SERBIAN, Language.SLOVENE, Language.LITHUANIAN, Language.LATVIAN,
        Language.ESTONIAN, Language.IRISH, Language.ICELANDIC,
        Language.UKRAINIAN
    ]
    
    detector = LanguageDetectorBuilder.from_languages(*languages).build()

    # Detect the language with the highest confidence
    result = detector.compute_language_confidence_values(question)

    if result:
        # Language with the highest confidence
        detected_language  = result[0].language  
        is_supported_language = detected_language in allowed_languages
        return is_supported_language

    return True
