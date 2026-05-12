import chromadb

# Persistent ChromaDB client
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Create or load collection
collection = client.get_or_create_collection(
    name="chat_memory"
)

# Store memory
def store_memory(text):

    try:

        collection.add(
            documents=[text],
            ids=[str(hash(text))]
        )

    except:
        pass

# Retrieve memory
def retrieve_memory(query):

    try:

        results = collection.query(
            query_texts=[query],
            n_results=2
        )

        return results["documents"][0]

    except:

        return []