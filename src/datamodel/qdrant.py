from typing import Any, List, Optional

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant.qdrant import QdrantVectorStore
from langchain_qdrant.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


class QdrantDatamodel:
    """
    Qdrant 資料模型：用來建立、檢查、以及操作 Qdrant 的向量資料庫
    """

    def __init__(self) -> None:
        pass

    def get_client(self) -> QdrantClient:
        """
        建立並回傳一個 QdrantClient 物件，連線到本機的 Qdrant。
        """
        return QdrantClient(host="localhost", port=6333)

    def check_client(self) -> None:
        """
        測試 Qdrant 是否可連線，並列出目前所有的 collections。
        """
        client = self.get_client()
        try:
            collections = client.get_collections()
            print("成功連線到 Qdrant！")
            print("目前集合：", collections)
        except Exception as e:
            print(f"連線到 Qdrant 失敗，錯誤訊息：{e}")

    def create(self, collection_name: str) -> None:
        """
        如果 collection 不存在，則建立新的 collection。
        預設向量大小 = 384，距離度量 = COSINE。
        """
        client = self.get_client()
        if not client.collection_exists(collection_name=collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

    def create_vectorstore(
        self, documents: List[Document], embedding: Embeddings, collection_name: str
    ) -> Qdrant:
        """
        由文件清單建立 Qdrant 向量資料庫並回傳 vectorstore。
        """
        vectorstore = Qdrant.from_documents(
            documents=documents,
            embedding=embedding,
            url="http://localhost:6333",
            collection_name=collection_name,
        )
        return vectorstore

    def get_vectorstore(
        self, client: QdrantClient, collection_name: str, embedding: Embeddings
    ) -> QdrantVectorStore:
        """
        取得既有 collection 的向量存取介面。
        """
        vectorstore = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embedding,
        )
        return vectorstore


# 初始化物件，可直接使用
qdrant_datamodel = QdrantDatamodel()
