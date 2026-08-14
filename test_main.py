"""
The file to be used to test the intermediate steps and modules at the time of development

"""

# Imports

from pdf_extractor import pdf_parser
from chunker import textSplitter


def main():

    # 1. Get the pdfs from the folder
    # 2. Build chunks using langchain
    # 3. Make embeddings
    # 4. Vectorize embeddings

    parsed_obj = pdf_parser("pdfs")
    pdf_obj = parsed_obj.get_page_information()
    chunks = textSplitter(pdf_obj)
    print(chunks)

    
if __name__ == "__main__":
    main()