from openai import OpenAI

from data_wellness_hackathon.config import cfg

client = OpenAI()


def get_embedding(text: str, model: str = cfg.embedding_model):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


if __name__ == "__main__":
    embedding = get_embedding("Today the weather is nice!")
    print("Embedding length", len(embedding))
