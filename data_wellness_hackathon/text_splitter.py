from typing import Iterator, Tuple, Callable
from pathlib import Path

from data_wellness_hackathon.config import cfg


def get_chunks(doc: Path, s: str, maxlength: int) -> Iterator[Tuple[str, str]]:
    start = 0
    end = 0
    while start + maxlength < len(s) and end != -1:
        end = s.rfind(" ", start, start + maxlength + 1)
        yield doc.stem, s[start:end]
        start = end + 1
    yield doc.stem, s[start:]


def get_chunks_overlap(doc: Path, s: str, maxlength: int, slide_back_divisor: int = 10) -> Iterator[Tuple[str, str]]:
    start = 0
    end = 0
    splits = s.split()
    split_len = len(splits)
    while start - maxlength // slide_back_divisor < split_len:
        end = start + maxlength + 1
        yield doc.stem, " ".join(splits[start:end])
        start = end + 1 - maxlength // slide_back_divisor # slide back by fraction of text


def split_text(maxlength: int = 100, chunks: Callable = get_chunks) -> Iterator[str]:
    for doc in cfg.doc_location.glob("*.txt"):
        text = doc.read_text(encoding="utf-8").strip()
        for chunk in chunks(doc, text, maxlength):
            yield chunk


if __name__ == "__main__":

    def get_chunks_split_20(doc: Path, s: str, maxlength: int):
        return get_chunks_overlap(doc, s, maxlength, 20)

    for t in split_text(200, get_chunks_split_20):
        print(" *************************** ")
        print(t)
