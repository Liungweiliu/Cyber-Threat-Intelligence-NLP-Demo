from fire import Fire
from langchain.chains import RetrievalQA

from src.datamodels.constant import COLLECTION_NAME
from src.datamodels.qdrant import qdrant_datamodel
from src.ingestion.load_data import download_file, load_json
from src.models.huggingface import get_embedding_model
from src.models.llm import get_llm_model


def ingest_collection(collection_name: str = COLLECTION_NAME) -> None:
    save_path = download_file()
    embedding = get_embedding_model()

    report = load_json(
        file_path=save_path,
        jq_schema='.data.attributes.sigma_analysis_results[] | {full_content: (.rule_title + " " + .rule_description + " " + .rule_level + " " + .rule_id), rule_id: .rule_id, rule_source: .rule_source, rule_title: .rule_title, rule_level: .rule_level, rule_description: .rule_description, rule_author: .rule_author, match_context: .match_context}',
        content_key="full_content",
    )
    qdrant_datamodel.create_collection(collection_name=collection_name)
    vectorstore = qdrant_datamodel.create_vectorstore(
        documents=report, embedding=embedding, collection_name=collection_name
    )


def main(collection_name: str = COLLECTION_NAME):
    embedding = get_embedding_model()
    client = qdrant_datamodel.create_client(host="localhost", port=6333)
    if not client.collection_exists(collection_name=collection_name):
        ingest_collection(collection_name=collection_name)

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
        answer = result.get("result")
        print(
            f"""{'':=>20} 
{query=} 
{answer=}"""
        )


if __name__:
    Fire({"main": main, "ingest_collection": ingest_collection})
# python -um demo ingest_collection
