"""Local, dependency-light Day 18 document loading and hierarchical chunking."""
from dataclasses import dataclass
from pathlib import Path
from config import DATA_DIR, HIERARCHICAL_PARENT_SIZE, HIERARCHICAL_CHILD_SIZE

@dataclass
class Chunk:
    text: str
    metadata: dict
    parent_id: str | None = None

def load_documents(data_dir: str = DATA_DIR) -> list[dict]:
    documents = []
    for path in Path(data_dir).glob("*.md"):
        documents.append({"text": path.read_text(encoding="utf-8"), "metadata": {"source": path.name}})
    return documents

def _split(text: str, size: int) -> list[str]:
    words, output, current = text.split(), [], []
    for word in words:
        current.append(word)
        if len(" ".join(current)) >= size:
            output.append(" ".join(current)); current = []
    if current:
        output.append(" ".join(current))
    return output

def chunk_basic(text: str, chunk_size: int = 500, metadata: dict | None = None) -> list[Chunk]:
    return [Chunk(part, metadata or {}) for part in _split(text, chunk_size)]

def chunk_hierarchical(text: str, parent_size: int = HIERARCHICAL_PARENT_SIZE,
                       child_size: int = HIERARCHICAL_CHILD_SIZE, metadata: dict | None = None):
    parents, children = [], []
    for index, parent_text in enumerate(_split(text, parent_size)):
        parent_id = f"{(metadata or {}).get('source', 'document')}:{index}"
        parents.append(Chunk(parent_text, metadata or {}, parent_id))
        children.extend(Chunk(child_text, metadata or {}, parent_id) for child_text in _split(parent_text, child_size))
    return parents, children
