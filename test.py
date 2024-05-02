from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.ollama import Ollama

import logging
import sys

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

models = [
    'llama3:8b',
    'gemma:7b',
    'phi3:3.8b'
]

print('Loading data...')
documents = SimpleDirectoryReader("test_pdfs").load_data()

# bge embedding model
Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

for model in models:
    # ollama
    Settings.llm = Ollama(model=model, request_timeout=30.0)

    # print('Creating vector store...')
    index = VectorStoreIndex.from_documents(
        documents,
    )

    query = 'Summarise the context'

    print(f'Running query: "{query}" with model: {model}')

    query_engine = index.as_query_engine(streaming=True)
    streaming_response = query_engine.query(query)
    streaming_response.print_response_stream()
    print()
    print('-'*20)