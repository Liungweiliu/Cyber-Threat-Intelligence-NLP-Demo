from langchain.chains import RetrievalQA

from src.datamodels.constant import COLLECTION_NAME
from src.datamodels.qdrant import QdrantClient, qdrant_datamodel
from src.models.huggingface import embedding_model
from src.models.llm import BaseChatModel, llm_model


def get_qa_model(
    llm_model: BaseChatModel,
    client: QdrantClient,
    collection_name: str = COLLECTION_NAME,
):
    vectorstore = qdrant_datamodel.get_vectorstore(
        client=client,
        collection_name=collection_name,
        embedding=embedding_model,
    )
    return RetrievalQA.from_chain_type(
        llm=llm_model, retriever=vectorstore.as_retriever(), chain_type="stuff"
    )


qa_model = get_qa_model(
    llm_model=llm_model, client=qdrant_datamodel.client, collection_name=COLLECTION_NAME
)
