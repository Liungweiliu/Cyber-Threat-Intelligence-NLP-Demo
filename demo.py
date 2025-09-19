import json
import os

import requests
from fire import Fire
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import JSONLoader
from langchain_community.llms import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from transformers import pipeline

from src.datamodel.qdrant import qdrant_datamodel


def get_embedding_model(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=model_name)


def _check_file_exist(path: str) -> bool:
    return os.path.exists(path)


def download_file(
    file_hash: str = "b5c001cbcd72b919e9b05e3281cc4e4914fee0748b3d81954772975630233a6e",
) -> str:
    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
    save_path = f"virustotal_report_{file_hash}.json"
    if _check_file_exist(path=save_path):
        print("File exists")
        return save_path
    # API 端點
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"

    headers = {"x-apikey": VIRUSTOTAL_API_KEY, "Accept": "application/json"}

    try:
        # 發送 GET 請求
        print(f"查詢檔案雜湊值: {file_hash}")
        response = requests.get(url, headers=headers)

        # 檢查回應狀態碼
        if response.status_code == 200:
            report = response.json()

            # 將 JSON 報告存檔
            with open(save_path, "w") as f:
                json.dump(report, f, indent=4)
            print(f"成功下載報告，已儲存為 virustotal_report_{file_hash}.json")

        elif response.status_code == 404:
            print(f"錯誤：找不到此檔案雜湊值 {file_hash} 的報告。")
        else:
            print(f"API 請求失敗，狀態碼：{response.status_code}")
            print(f"回應內容：{response.text}")

    except requests.exceptions.RequestException as e:
        print(f"發生網路錯誤: {e}")
    return save_path


def get_llm_model():
    import getpass
    import os

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

    from langchain.chat_models import init_chat_model

    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    return llm


def get_hf_llm_model() -> HuggingFacePipeline:
    hf_pipeline = pipeline("text-generation", model="distilgpt2", max_new_tokens=100)
    llm = HuggingFacePipeline(pipeline=hf_pipeline)
    return llm


# Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:
    columns = [
        "rule_level",
        "rule_id",
        "rule_source",
        "rule_title",
        "rule_description",
        "rule_author",
        "match_context",
    ]
    for column in columns:
        metadata[column] = record.get(column)
    return metadata


def main(collection_name: str = "sigma_analysis_collection"):
    save_path = download_file()
    client = qdrant_datamodel.get_client()
    embedding = get_embedding_model()

    if not client.collection_exists(collection_name=collection_name):
        loader = JSONLoader(
            file_path=save_path,
            jq_schema=".data.attributes.sigma_analysis_results[]",
            content_key="rule_description",
            metadata_func=metadata_func,
        )
        report = loader.load()
        qdrant_datamodel.create(collection_name=collection_name)
        vectorstore = qdrant_datamodel.create_vectorstore(
            documents=report, embedding=embedding, collection_name=collection_name
        )

    else:
        print(f"{'':=>20} {collection_name=} exist, connect without create.")
        embedding = get_embedding_model()
        vectorstore = qdrant_datamodel.get_vectorstore(
            client=client,
            collection_name=collection_name,
            embedding=embedding,
        )

    llm = get_llm_model()

    qa = RetrievalQA.from_chain_type(
        llm=llm, retriever=vectorstore.as_retriever(), chain_type="stuff"
    )

    questions = [
        "Give me a short and precise summary about the report.",
        "Can you tell me about the malicious use of Microsoft Word and COM objects?",
    ]

    for question in questions:
        result = qa.invoke(question)
        query = result.get("query")
        result = result.get("result")
        print(
            f"""{'':=>20} 
{query=} 
{result=}"""
        )


if __name__:
    Fire({"main": main})
# python -um demo main
