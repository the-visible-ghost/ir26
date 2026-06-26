from typing import List
from fastembed import TextEmbedding
import numpy as np
from . import debug


class Embedder:
    def __init__(self, model: str) -> None:
        self._embedder: TextEmbedding = TextEmbedding(model)

    @debug
    def embed(self, texts: str | List[str]) -> np.ndarray:
        return np.array(list(self._embedder.embed(texts)))
