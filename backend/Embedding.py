
from sentence_transformers import SentenceTransformer

#ML Model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

#Memory from database
memory = "I met Susan at the community center. She teaches yoga."

#Converting sentences into verticies
embedding = model.encode(memory)

print("Original memory:", memory)
print("Vector dimensions:", len(embedding))
print("First 10 numbers:", embedding[:10])
