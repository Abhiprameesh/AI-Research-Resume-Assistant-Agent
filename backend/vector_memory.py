import chromadb

client = chromadb.Client()

collection = client.create_collection(
    name="chat_memory"
)

def store_memory(text):

    collection.add(
        documents=[text],
        ids=[str(hash(text))]
    )

def retrieve_memory(query):

    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    return results["documents"][0]