from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
)
from llama_index.core.embeddings import resolve_embed_model

Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

# load documents
documents = SimpleDirectoryReader("./test_pdfs_2").load_data()

index = VectorStoreIndex.from_documents(documents)

# save index to disk
index.set_index_id("vector_index")
index.storage_context.persist("./storage")