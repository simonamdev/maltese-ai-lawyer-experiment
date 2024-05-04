import json
import matplotlib.pyplot as plt

# Load your embeddings (e.g., from a CSV file)
vector_store_path = './storage/default__vector_store.json'

with open(vector_store_path, 'r') as f:
    data = json.loads(f.read())

# COVID
embeddings_1 = data['embedding_dict']['f1492a92-5be6-4f83-916f-61bc9e3a0311']
embeddings_2 = data['embedding_dict']['25146985-53cb-41eb-bceb-2d2e79fc4e36']
embeddings_3 = data['embedding_dict']['966932f4-0ca5-475a-92cf-be25a1031c50']

# Architects
embeddings_4 = data['embedding_dict']['102234f5-dcd6-4854-be59-e361ecd9b96e']

# Stipend
embeddings_5 = data['embedding_dict']['33c9b165-d66e-4a34-9291-3e9b3010b424']

# Create a scatter plot
plt.scatter(embeddings_1, embeddings_2,  c='blue')
plt.scatter(embeddings_1, embeddings_3,  c='cyan')
plt.scatter(embeddings_1, embeddings_4,  c='red')
plt.scatter(embeddings_1, embeddings_5,  c='green')
plt.xlabel('Array 1')
plt.ylabel('Array 2')
plt.gca().set_xlim(-0.15, 0.15)
plt.gca().set_ylim(-0.15, 0.15)
plt.show()
