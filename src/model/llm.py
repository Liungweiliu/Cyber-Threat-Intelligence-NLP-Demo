import getpass
import os

from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline


def get_llm_model():
    """
    建立並回傳 OpenAI 的 LLM 模型（使用 langchain.chat_models.init_chat_model）。
    若環境變數中沒有 OPENAI_API_KEY，會提示使用者輸入。

    Returns:
        BaseLanguageModel: 初始化完成的 OpenAI 聊天模型
    """
    if not os.environ.get("OPENAI_API_KEY"):
        # 若沒有 API key，就要求輸入
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

    from langchain.chat_models import init_chat_model

    # 初始化指定的模型（gpt-4o-mini）
    return init_chat_model("gpt-4o-mini", model_provider="openai")


def get_hf_llm_model() -> HuggingFacePipeline:
    """
    建立並回傳 Hugging Face 的 LLM 模型，包裝為 HuggingFacePipeline。

    Returns:
        HuggingFacePipeline: HuggingFace text-generation pipeline 的封裝
    """
    hf_pipeline = pipeline("text-generation", model="distilgpt2", max_new_tokens=50)

    llm: HuggingFacePipeline = HuggingFacePipeline(pipeline=hf_pipeline)
    return llm
