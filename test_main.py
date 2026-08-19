"""
The file to be used to test the intermediate steps and modules at the time of development

"""

# Imports

from pdf_extractor import pdf_parser
from chunker import chunker
from embedder import embedder


def main():

    # 1. Get the pdfs from the folder
    # 2. Build chunks using langchain
    # 3. Make embeddings
    # 4. Vectorize embeddings

    parsed_obj = pdf_parser("pdfs")
    pdf_obj = parsed_obj.get_page_information()
    chunker_class_instance = chunker(pdf_obj)
    chunks = chunker_class_instance.chunksFromJson()
    embeddings_generator=embedder(chunks)
    embeddings_generator.embedding_and_database()

    # for i, indi_embeddings in enumerate(embeddings_list):
    #     if i==3: 
    #         #print(indi_embeddings.len()) 
    #         print(type(indi_embeddings))

    # Once the documents are added in the chormaDB, write a short query here to check the retrival capabalities of the embeddings. 

    

    
if __name__ == "__main__":
    main()