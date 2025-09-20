import os
from typing import List

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant.qdrant import QdrantVectorStore
from langchain_qdrant.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))


class QdrantDatamodel:

    def __init__(self) -> None:
        self.client = self.create_client()

    def create_client(
        self, host: str = QDRANT_HOST, port: int = QDRANT_PORT
    ) -> QdrantClient:
        return QdrantClient(host=host, port=port)

    def check_client(self) -> None:
        try:
            collections = self.client.get_collections()
            print(f"{collections=}", collections)
        except Exception as e:
            print(f"Fail to connect to Qdrant Error：{e}")

    def create_collection(self, collection_name: str, size: int = 384) -> None:
        if not self.client.collection_exists(collection_name=collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE),
            )

    def create_vectorstore(
        self, documents: List[Document], embedding: Embeddings, collection_name: str
    ) -> Qdrant:
        vectorstore = Qdrant.from_documents(
            documents=documents,
            embedding=embedding,
            url=f"http://{QDRANT_HOST}:{QDRANT_PORT}",
            collection_name=collection_name,
        )
        return vectorstore

    def get_vectorstore(
        self, client: QdrantClient, collection_name: str, embedding: Embeddings
    ) -> QdrantVectorStore:
        vectorstore = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embedding,
        )
        return vectorstore


qdrant_datamodel = QdrantDatamodel()
