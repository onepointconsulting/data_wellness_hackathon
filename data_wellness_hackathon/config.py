import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    neon_connection = os.getenv("NEON_CONNECTiON")
    assert neon_connection is not None, "NEON_CONNECTiON is mandatory."
    doc_location_str = os.getenv("DOC_LOCATION")
    assert doc_location_str is not None, "DOC_LOCATION cannot be empty."
    doc_location = Path(doc_location_str)
    assert (
        doc_location.exists()
    ), f"Document location folder {doc_location} does not exist."
    embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    split_size_str = os.getenv("SPLIT_SIZE")
    assert split_size_str is not None, "Split size needs to be defined as integer"
    split_size = int(split_size_str)


cfg = Config()

if __name__ == "__main__":
    assert cfg.neon_connection is not None
    print(cfg.doc_location)
    print(cfg.embedding_model)
