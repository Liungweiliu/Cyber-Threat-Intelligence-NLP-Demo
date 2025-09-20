import getpass
import os

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel


def get_llm_model(
    model: str = "gpt-4o-mini", model_provider: str = "openai"
) -> BaseChatModel:
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

    return init_chat_model(model=model, model_provider=model_provider)


llm_model = get_llm_model()
