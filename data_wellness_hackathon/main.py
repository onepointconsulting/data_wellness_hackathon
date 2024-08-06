import asyncio

from data_wellness_hackathon.config import cfg
from data_wellness_hackathon.text_splitter import split_text
from data_wellness_hackathon.embeddings import get_embedding
from data_wellness_hackathon.persistence import insert_embeddings

def insert_vectors() -> int:
    count = 0
    for title, text in split_text(cfg.split_size):
        embedding = get_embedding(text)
        asyncio.run(insert_embeddings(title, text, embedding))
        count += 1
    return count

if __name__ == "__main__":
    processed = insert_vectors()
    print(f"Processed {processed} documents")