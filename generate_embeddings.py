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

from redisvl.schema import IndexSchema

from llama_index.llms.ollama import Ollama

Settings.llm = Ollama(model='gemma:7b', request_timeout=300.0)

custom_schema = IndexSchema.from_dict(
    {
        # customize basic index specs
        "index": {
            "name": "malta_laws",
            "prefix": "mal",
            "key_separator": ":",
        },
        # customize fields that are indexed
        "fields": [
            # required fields for llamaindex
            {"type": "tag", "name": "id"},
            {"type": "tag", "name": "doc_id"},
            {"type": "text", "name": "text"},
            # custom metadata fields
            {"type": "numeric", "name": "updated_at"},
            {"type": "tag", "name": "file_name"},
            # custom vector field definition for cohere embeddings
            {
                "type": "vector",
                "name": "vector",
                "attrs": {
                    "dims": 384,
                    "algorithm": "hnsw",
                    "distance_metric": "cosine",
                },
            },
        ],
    }
)

logging.basicConfig(format='%(asctime)s %(message)s',
                    encoding='utf-8', level=logging.INFO)

logging.info('Loading embedding model...')
Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

logging.info('Connecting to redis....')
# create a Redis client connection
redis_client = Redis.from_url("redis://localhost:6379")

# create the vector store wrapper
vector_store = RedisVectorStore(
    redis_client=redis_client, overwrite=True, schema=custom_schema)

# load storage context
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# load documents
logging.info('Loading documents...')
documents = SimpleDirectoryReader(
    "./pdfs", num_files_limit=2).load_data(show_progress=True)

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
