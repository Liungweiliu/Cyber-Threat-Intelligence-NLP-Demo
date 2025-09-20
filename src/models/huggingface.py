from langchain_community.llms import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline


def get_hf_llm_model(
    task: str = "text-generation", model: str = "distilgpt2", max_new_tokens: int = 50
) -> HuggingFacePipeline:
    hf_pipeline = pipeline(
        "text-generation", model=model, max_new_tokens=max_new_tokens
    )

    llm: HuggingFacePipeline = HuggingFacePipeline(pipeline=hf_pipeline)
    return llm


def get_embedding_model(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=model_name)


embedding_model = get_embedding_model()
