import os
import pandas as pd
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

QDRANT_PATH = os.path.join(os.path.dirname(__file__), "../qdrant_db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/headphones.csv")
COLLECTION = "headphones"


def ingest(api_key: str) -> QdrantVectorStore:
    """Embed headphones CSV into Qdrant (persisted to disk)."""
    df = pd.read_csv(CSV_PATH)

    documents = []
    metadatas = []

    for _, row in df.iterrows():
        text = (
            f"Product: {row['name']} by {row['brand']}. "
            f"Price: ₹{row['price_inr']}. "
            f"Category: {row['category']}. "
            f"Connectivity: {row['connectivity']}. "
            f"Rating: {row['rating']}/5. "
            f"Stock: {row['stock']} units. "
            f"Battery: {row['battery_hours']} hours. "
            f"Noise Cancellation: {row['noise_cancellation']}. "
            f"{row['description']}"
        )
        documents.append(text)
        metadatas.append({
            "id": row["id"],
            "name": row["name"],
            "brand": row["brand"],
            "price_inr": int(row["price_inr"]),
            "rating": float(row["rating"]),
            "stock": int(row["stock"]),
            "noise_cancellation": row["noise_cancellation"],
            "connectivity": row["connectivity"],
        })

    embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    vectorstore = QdrantVectorStore.from_texts(
        texts=documents,
        embedding=embeddings,
        metadatas=metadatas,
        collection_name=COLLECTION,
        path=QDRANT_PATH,
    )
    return vectorstore


def load(api_key: str) -> QdrantVectorStore:
    """Load existing Qdrant vector store from disk."""
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    client = QdrantClient(path=QDRANT_PATH)

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION,
        embedding=embeddings,
    )
    return vectorstore
