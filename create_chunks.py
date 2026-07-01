import os
import json

CHUNK_SIZE = 90 * 1024 * 1024

target_files = [
    # Index files
    "processed/experience_index.faiss",
    "processed/skills_index.faiss",
    "processed/summary_index.faiss",
    # Vector files
    "processed/summary_vectors.npy",
    "processed/skills_vectors.npy",
    "processed/experience_vectors.npy",
    # Models
    "models/ms-marco-MiniLM-L-12-v2/model.safetensors",
]

chunks_data = {}


for file in target_files:
    with open(file, "rb") as fp:
        data = fp.read()

    chunks_data[file] = []

    for idx, start in enumerate(range(0, len(data), CHUNK_SIZE)):
        filename = f"./chunks/{file}.{idx}"

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "wb") as fp:
            fp.write(data[start : start + CHUNK_SIZE])
        chunks_data[file].append(filename)

with open("./chunks_data.json", "w") as fp:
    json.dump(chunks_data, fp, indent=4)
