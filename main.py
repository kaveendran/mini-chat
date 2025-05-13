from src.config.settings import EMBEDDING_MODEL
import sys
for i in sys.path:
    print(i)
print(EMBEDDING_MODEL)

from src.scripts.ingest import main

main()