# maltese-ai-lawyer-experiment

Can we create a Maltese AI Lawyer? This is the code used for the 6th May 2024 GDG session about using LLMs and RAG to answer questions about Maltese legislation.

# Required tech

- Miniconda
- Ollama: https://github.com/ollama/ollama

# Setup

- conda create -n mal
- conda activate mal
- conda install pip
- pip install llama-index
  (Note: llama-index was at 0.10.33 at time of writing)
- pip install llama-index-core llama-index-readers-file llama-index-llms-ollama llama-index-embeddings-huggingface
- ollama pull llama3:8b
- ollama pull gemma:7b
- ollama pull phi3:3.8b
- python3 test.py

# Persistence

Test and visualise embeddings generated

- pip install matplotlib
- python test_build_vector_store.py
- python visualise_embeddings.py
