import os
from typing import Union
from utils.logging import log
from promptflow.core import tool
from promptflow.connections import AzureOpenAIConnection, OpenAIConnection
from typing import Dict, Any


def build_pdf_path(pdf_name:str):
    return f"./pdfs/{pdf_name}"


@tool
def setup_env(connection: Union[AzureOpenAIConnection, OpenAIConnection], config: dict,pdf_name:str, vector_db:str,use_history:bool) -> Dict[str,any]:
    try:
        if not connection or not config:
            log("Connection or config is missing.")
            return False

        if isinstance(connection, AzureOpenAIConnection):
            os.environ["OPENAI_API_TYPE"] = "azure"
            os.environ["OPENAI_API_BASE"] = connection.api_base
            os.environ["OPENAI_API_KEY"] = connection.api_key
            os.environ["OPENAI_API_VERSION"] = connection.api_version

        elif isinstance(connection, OpenAIConnection):
            os.environ["OPENAI_API_KEY"] = connection.api_key
            if connection.organization is not None:
                os.environ["OPENAI_ORG_ID"] = connection.organization

        for key, value in config.items():
            os.environ[key] = str(value)

        return {'pdf_path':build_pdf_path(pdf_name),'vector_db':vector_db,'use_history':use_history,'env_ready':True}

    except Exception as e:
        log(f"Error setting up environment: {e}")
        return False
