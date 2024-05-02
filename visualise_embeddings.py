import json
import matplotlib.pyplot as plt

# Load your embeddings (e.g., from a CSV file)
vector_store_path = './storage/default__vector_store.json'

with open(vector_store_path, 'r') as f:
    data = json.loads(f.read())

# COVID
embeddings_1 = data['embedding_dict']['40be887e-91bf-47f4-b079-96894c4530c3']
embeddings_2 = data['embedding_dict']['db758dcd-d8a9-497a-a42d-a3851863da1f']

# Architects
embeddings_3 = data['embedding_dict']['1b2545b7-9083-4cb6-a6ad-6fdfd868e8e5']

# Stipend
embeddings_4 = data['embedding_dict']['1a0b9e12-f742-477d-a026-f8dc14db512f']

# Create a scatter plot
plt.scatter(embeddings_1, embeddings_2,  c='blue')
plt.scatter(embeddings_1, embeddings_3,  c='red')
plt.scatter(embeddings_1, embeddings_4,  c='green')
plt.xlabel('Array 1')
plt.ylabel('Array 2')
plt.gca().set_xlim(-0.1, 0.1)
plt.gca().set_ylim(-0.1, 0.1)
plt.show()
