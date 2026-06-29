from typing import List
from fastembed import TextEmbedding
import numpy as np
from . import debug


class Embedder:
    @debug
    def __init__(self, name: str, path: None | str = None) -> None:
        self._embedder: TextEmbedding = TextEmbedding(name, model_dir=path)

    @debug
    def embed(self, texts: str | List[str]) -> np.ndarray:
        return np.array(list(self._embedder.embed(texts)))
