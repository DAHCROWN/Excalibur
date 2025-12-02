import os
import uuid
from pathlib import Path
from typing import List, Dict, Any

from pinecone import Pinecone

from rag.embeddings import PineconeEmbeddingEngine as EmbeddingEngine
from models.datasets import NigerianFraudDataset, SpamAssasinDataset, LingDataset, EmailRecord

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pandas as pd
# -----------------------------
# CONFIG
# -----------------------------
DATASET_DIR = "../datasets/"
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "fraud-email-index"
# -----------------------------
# DATASET REGISTRY
# -----------------------------
DATASET_REGISTRY = {
    "nigerian_fraud": {
        "model": NigerianFraudDataset,
        "path": "datasets/nigerian_fraud.csv",
    },
    # "spam_assassin": {
    #     "model": SpamAssasinDataset,
    #     "path": "datasets/spam_assassin.csv",
    # },
    # "ling_spam": {
    #     "model": LingDataset,
    #     "path": "datasets/ling_spam.csv",
    # },
    # # Generic fallback dataset
    # "generic": {
    #     "model": EmailRecord,
    #     "path": None,  # When loading automatically from folder
    # }
}

# -----------------------------
# Load + Validate CSV Records
# -----------------------------
def load_csv_records() -> List[Any]:
    dataset_path = Path(DATASET_DIR)
    validated = []

    # Load datasets explicitly defined in registry
    for name, cfg in DATASET_REGISTRY.items():
        model = cfg["model"]
        file_path = cfg["path"]

        if file_path:
            fp = Path(file_path)
            if fp.exists():
                print(f"[INGEST] Loading dataset '{name}' from {fp}...")

                df = pd.read_csv(file_path)
                # TODO increase to index the full dataset
                docs = df.head(10).to_dict(orient='records')
                # print(docs[0])
                for doc in docs:
                    try:        # <- THIS is a dict
                        validated.append(model(**doc))
                    except Exception as e:
                        print(f"[WARN] Skipping invalid row in {name}: {e}")


    # Auto‑load any other CSV in datasets folder using the generic EmailRecord schema
    for file in dataset_path.glob("*.csv"):
        if any(cfg["path"] == str(file) for cfg in DATASET_REGISTRY.values()):
            continue

        print(f"[INGEST] Auto-loading generic CSV: {file}")
        loader = CSVLoader(str(file))
        docs = loader.load()
        for doc in docs:
            row = doc.metadata
            try:
                validated.append(EmailRecord(**row))
            except Exception as e:
                print(f"[WARN] Skipping invalid generic row: {e}")

    print(f"[INGEST] Loaded {len(validated)} validated rows from all datasets.")
    return validated
    
# -----------------------------
# Build Pinecone Datapoints
# -----------------------------
def build_pinecone_datapoints(records: List[Any], embeddings: List[List[float]]):
    datapoints = []

    for record, vector in zip(records, embeddings):
        datapoints.append({
            "id": str(uuid.uuid4()),
            "values": vector['values'],
            "metadata": {
                "sender": record.sender,
                "receiver": record.receiver,
                "subject": record.subject,
                "body": record.body,
                "urls": record.urls,
                "label": record.label or "",
            }
        })

    return datapoints


# -----------------------------
# Upload to Pinecone Vector Store
# -----------------------------
def upload_to_pinecone(datapoints: List[Dict[str, Any]]):
    # print("[PINECONE] Uploading vectors...")
    # print(datapoints)
    # return

    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Create if not found
    if not pc.has_index(PINECONE_INDEX_NAME):
        print("[PINECONE] Index does not exist, creating...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=len(datapoints[0]["values"]),
            metric="cosine",
            spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
        )

    index = pc.Index(PINECONE_INDEX_NAME)
    index.upsert(vectors=datapoints)

    print("[PINECONE] Upload successful.")


# -----------------------------
# Main Ingest Function
# -----------------------------
def ingest():
    # Helper Function
    def _prepare_text(record):
        body = record.body or ""
        # Truncate extremely long bodies to reduce payload size
        if len(body) > MAX_BODY_CHARS:
            body = body[:MAX_BODY_CHARS]
        return body

    print("[INGEST] Starting...")

    #* Step 1 — Load + validate CSV
    records = load_csv_records()
    # If there is nothing to embed, exit early to avoid invalid requests
    if not records:
        print("[INGEST] No records loaded; nothing to embed or upload.")
        return

    # Step 2 — Embed bodies
    embedder = EmbeddingEngine()
    print("[INGEST] Generating embeddings...")

    MAX_BODY_CHARS = 2000  # soft limit to keep requests reasonable in size
    BATCH_SIZE = 10     # adjust based on body lengths and limits


    all_embeddings = []
    for start in range(0, len(records), BATCH_SIZE):
        batch_records = records[start:start + BATCH_SIZE]
        batch_texts = [_prepare_text(r) for r in batch_records]

        # Defensive check – should not be empty, but guard anyway
        if not batch_texts:
            continue

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        texts = text_splitter.split_text(batch_texts[0])
        batch_embeddings = embedder.embed(texts)
        # batch_embeddings = embedder.embed(batch_texts)

        # Some client versions / error paths may return None instead of a list.
        # Guard against that so we don't hit "NoneType is not iterable".
        if not batch_embeddings:
            print(f"[INGEST] Warning: received no embeddings for batch starting at index {start}, skipping.")
            continue

        all_embeddings.extend(batch_embeddings)

    embeddings = all_embeddings
    # print("embeddings")
    # print(embeddings)

    # Step 3 — Build datapoints
    datapoints = build_pinecone_datapoints(records, embeddings)

    # Step 4 — Upload to Pinecone Vector Store
    upload_to_pinecone(datapoints)

    print("[INGEST] Done!")


if __name__ == "__main__":
    ingest()


# python3 -m rag.ingest