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
import json
from llm_api import LLMAPI

# Constants:
# TBD: Change this so that this value is accepted from the GUI.  
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

    output_document_lst = result.get("documents")
    # Add context from the retrieved documents
    CONTEXT = " "
    for info in output_document_lst[0]:
        CONTEXT =  CONTEXT+info 

    # Identify the references for citations. 
    document_name_lst = []
    image_paths = []
    page_numbers_lst=[]
    output_metadata_lst = result.get("metadatas")[0]
    for individual_metadata in output_metadata_lst: 
        document_name_lst.append(individual_metadata.get("document_name"))
        image_paths_lst = json.loads(individual_metadata.get("image_paths"))
        page_numbers_lst.append(individual_metadata.get("page_number"))
        # Do only if there are reference images present:
        if len(image_paths_lst)!=0: 
            image_paths.extend(image_paths_lst)

    # Calling LLM API with context: 
    api_call = LLMAPI()

    answer = api_call.generate_answer(question=QUERY_TEXT, 
                                      context=CONTEXT)
    print(answer)
    
    
if __name__ == "__main__":
    main()
    