import constants
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import sys
import socket

OpenAI_API_KEY = "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"
# Constants for OpenAI models
GPT35_TURBO = "gpt-3.5-turbo"
GPT4_TURBO = "gpt-4-0125-preview"


def initialize_chromadb_client():
    """
    Initializes and returns a ChromaDB client.
    """
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        model_name="text-embedding-3-small",
        api_key=OpenAI_API_KEY,
    )
    chroma_client = chromadb.PersistentClient()
    return chroma_client, embedding_function


def get_or_create_collection(client, collection_name, embedding_function):
    """
    Gets or creates a collection in ChromaDB with the specified name and embedding function.
    """
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )


def populate_collection_from_file(collection, file_path):
    """
    Populates a ChromaDB collection with data from a specified file.
    """
    if collection.count() == 0:
        with open(file_path, "r") as file:
            lines = file.readlines()
            print(f"Inserting {len(lines)} lines into the collection")
            for i, line in enumerate(lines):
                line = line.strip()
                item = line.split(".")[0]
                collection.upsert(ids=str(i + 1), documents=line, metadatas={"line_number": i + 1, "item": item})
            print(f"Inserted {collection.count()} lines into the collection")


def perform_semantic_search(collection, query, n_results=5):
    """
    Performs a semantic search on the given collection using the specified query.
    """
    db_result = collection.query(query_texts=query, n_results=n_results)
    print(db_result)
    # Print the items and the distance
    print(f"\nRetrieved rules:")
    print(f"     Dist.:  | Item:")
    for i, document in enumerate(db_result['documents'][0]):
        distance = db_result['distances'][0][i]
        item = db_result['metadatas'][0][i].get("item")
        # Format the index as i+1 with a fixed width of 2
        print(f"{i + 1:2} | {distance:.5f} | {item}")
    return db_result


def initialize_openai_client():
    """
    Initializes and returns an OpenAI client.
    """
    return OpenAI(api_key=OpenAI_API_KEY)


def generate_rag_response(client, rules, query, conn, model=GPT4_TURBO):
    """
    Generates a RAG response using the OpenAI Chat API.
    """
    system_message = f"""
    You are a helpful airline travel assistant specializing in TSA baggage rules.

    These rules might be relevant to the users query:
    ---
    {rules}
    ---
    Do ONLY answer the users query based on the rules provided.
    Do ONLY include rules that are relevant to the users query.
    Do NOT include irrelevant rules.

    Answer politely, professionally, and concise.
    """.strip()


    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ],
        stream=True
    )

    response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        output = content or ""
        conn.send(output.encode())
        print("Skal sende: \n", output)
        response += content or ""
        sys.stdout.write(content or "")  # Write the content to the console
    # Close the stream
    sys.stdout.flush()
    return response


def run(query, conn):
    chroma_client, embedding_function = initialize_chromadb_client()
    collection = get_or_create_collection(chroma_client, "semantic-search-demo-oai", embedding_function)
    populate_collection_from_file(collection, "/Users/ap/PycharmProjects/smartpackproject/config/data/avinor_rules.txt")

    #query = "Kan jeg ta med kniv?"
    print(query)
    db_result = perform_semantic_search(collection, query)
    rules = "\n".join(db_result['documents'][0])

    openai_client = initialize_openai_client()
    response = generate_rag_response(openai_client, rules, query, conn)
    return response





