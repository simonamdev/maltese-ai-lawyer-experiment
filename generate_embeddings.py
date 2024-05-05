from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
)
from llama_index.core.embeddings import resolve_embed_model
from llama_index.vector_stores.redis import RedisVectorStore

import logging

from llama_index.core import StorageContext
from redis import Redis


logging.basicConfig(format='%(asctime)s %(message)s',
                    encoding='utf-8', level=logging.INFO)

logging.info('Loading embedding model...')
Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

logging.info('Connecting to redis....')
# create a Redis client connection
redis_client = Redis.from_url("redis://localhost:6379")

# create the vector store wrapper
vector_store = RedisVectorStore(redis_client=redis_client, overwrite=True)

# load storage context
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# load documents
logging.info('Loading documents...')
documents = SimpleDirectoryReader(
    "./pdfs").load_data(show_progress=True)

# build and load index from documents and storage context
logging.info('Creating Index...')
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

query_engine = index.as_query_engine()
retriever = index.as_retriever()

result_nodes = retriever.retrieve("Covid laws in Malta")
for node in result_nodes:
    print(node)
