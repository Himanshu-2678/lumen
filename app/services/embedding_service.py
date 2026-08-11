from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def generate_embeddings(chunks: list[dict]) -> list[dict]:
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts, normalize_embeddings=True)
    print("EMBEDDINGS GENERATED:", len(embeddings))
    result = []
    for chunk, embedding in zip(chunks, embeddings):
        result.append({
            **chunk,
            "embedding": embedding.tolist()
        })  
    print("FIRST EMBEDDING SIZE:", len(result[0]["embedding"]))

    return result
