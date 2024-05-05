from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
)
from llama_index.core.embeddings import resolve_embed_model
from llama_index.vector_stores.redis import RedisVectorStore

import logging
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import StorageContext
from redis import Redis

from redisvl.schema import IndexSchema

from llama_index.llms.ollama import Ollama

logging.basicConfig(format='%(asctime)s %(message)s',
                    encoding='utf-8', level=logging.INFO)

logging.info('Starting LLM...')

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


logging.info('Loading embedding model...')
Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

logging.info('Connecting to redis....')
# create a Redis client connection
redis_client = Redis.from_url("redis://localhost:6379")

# create the vector store wrapper
logging.info('Creating Vector Store....')
vector_store = RedisVectorStore(
    redis_client=redis_client, schema=custom_schema
)

logging.info('Loading index...')
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store)

logging.info('Starting chat engine...')
memory = ChatMemoryBuffer.from_defaults(token_limit=10000)

chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=(
        "You are a Maltese Law AI assistant. You are able to answer questions about Maltese law from the given context."
    ),
    similarity_top_k=5
)

chat_engine.streaming_chat_repl()
