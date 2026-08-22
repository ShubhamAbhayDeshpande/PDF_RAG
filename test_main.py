"""
The file to be used to test the intermediate steps and modules at the time of development

"""

# Imports

from pdf_extractor import pdf_parser
from chunker import chunker
from embedder import embedder
import chromadb
import os
import retriever

# Constants: 
QUERY_TEXT = "What is IP-Mask and how to use it?"

def main():

    # 1. Get the pdfs from the folder
    # 2. Build chunks using langchain
    # 3. Make embeddings
    # 4. Vectorize embeddings

    # Check if the chormadb exists: 
    collection=None
    client = chromadb.PersistentClient(path=r"chroma_db")
    collection = client.get_collection(name="pdf_collection")

    if collection is None:
        parsed_obj = pdf_parser("pdfs")
        pdf_obj = parsed_obj.get_page_information()
        chunker_class_instance = chunker(pdf_obj)
        chunks = chunker_class_instance.chunksFromJson()
        embeddings_generator=embedder(chunks)
        embeddings_generator.embedding_and_database()

    # Make an embedding method using the langchain 
    retriever_function = retriever.retriever()
    query = retriever_function.query_embedding(QUERY_TEXT)

    result = collection.query(
        query_embeddings=query,
        n_results=5
    )

    print(len(result.get("metadatas")[0])) 
    
if __name__ == "__main__":
    main()