import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Create ChromaDB client
client = chromadb.PersistentClient(path="chroma_db")


# Create (or get) collection
collection = client.get_or_create_collection(
    name="resume_collection"
)


# Load embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

def store_resume(resume_text):

    # Split the resume into chunks
    chunks = text_splitter.split_text(resume_text)

    # Clear old resume (for now)
    try:
        client.delete_collection("resume_collection")
    except:
        pass

    global collection

    collection = client.get_or_create_collection(
        name="resume_collection"
    )

    for i, chunk in enumerate(chunks):

        embedding = embedding_model.encode(chunk).tolist()

        collection.add(
            ids=[str(i)],
            documents=[chunk],
            embeddings=[embedding]
        )

    print("Resume stored successfully!")


def retrieve_resume(query):

    # Convert question into embedding
    query_embedding = embedding_model.encode(
        query
    ).tolist()

    # Search similar resume chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    # Combine retrieved chunks
    context = "\n".join(
        results["documents"][0]
    )

    return context