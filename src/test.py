import sys
from config.settings import EMBEDDING_MODEL
from scripts.embeddings import create_embeddings



list = ["hello", "world"]
emb = create_embeddings("hello")
print(emb)


for i in sys.path:
    print(i)

print("x")
print(EMBEDDING_MODEL)