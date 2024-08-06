from typing import Iterator, Tuple
from pathlib import Path

from data_wellness_hackathon.config import cfg


def split_text(maxlength: int = 100) -> Iterator[str]:
    for doc in cfg.doc_location.glob("*.txt"):
        text = doc.read_text(encoding="utf-8").strip()
        for chunk in get_chunks(doc, text, maxlength):
            yield chunk


def get_chunks(doc: Path, s: str, maxlength: int) -> Iterator[Tuple[str, str]]:
    start = 0
    end = 0
    while start + maxlength < len(s) and end != -1:
        end = s.rfind(" ", start, start + maxlength + 1)
        yield doc.stem, s[start:end]
        start = end + 1
    yield doc.stem, s[start:]


if __name__ == "__main__":
    for t in split_text(2048):
        print(" *************************** ")
        print(t)
