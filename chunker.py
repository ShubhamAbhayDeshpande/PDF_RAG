"""
The program will create chunks from the text and images in the pdf file. 

Creator: Shubham Deshpande
Version: 0.0

"""
# Imports
import json
from pathlib import Path
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class chunker:
    """
    This class will accept string object as an input and it will do the chunking for the text and return the 
    splitted text as output. 
    
    """
    def __init__(self, jsonObj: dict, chunkSize: int=1000, chunkOverlap: int =20):
        self.jsonObj=jsonObj
        self.chunkSize=chunkSize
        self.chunkOverlap=chunkOverlap

    def chunksFromJson(self)-> list:
        """
        This function will accept the json object created from the document as an input and it will output a document 
        object used in the text splitter later. 
        
        """
        # we can directly parse the document because I know the structure for the json object. 
        document_list = []

        for doc_num, document_name in enumerate(self.jsonObj.keys()):
             # meta_data = dict()
             for pages_key in self.jsonObj[document_name].keys():
                meta_data = dict()
                # Assign the dictionary of all the page contents to a new dictionary for easier use. 
                page_data = self.jsonObj[document_name][pages_key]

                image_xrfs = list()
                image_paths = list()

                if  page_data.get("page_images"):
                    for images in page_data["page_images"]:
                        image_xrfs.append(images["xref"])
                        image_paths.append(images["image_path"])

                meta_data["document_name"] = document_name
                meta_data["page_number"] = int(pages_key)
                meta_data["chunk_id"]="doc"+str(doc_num)+"_"+str(pages_key)
                meta_data["image_ids"]=image_xrfs
                meta_data["image_paths"]=image_paths 

                # The following function makes only the list of document objects
                document_list.append(
                    Document(page_content=page_data.get("text", ""), 
                             metadata=meta_data
                             )
                        )
        # The list of document objects is converted to Chunks using the text splitter below.
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunkSize, 
                                                       chunk_overlap=self.chunkOverlap
                                                       )

        # The split_documents method can take list of document_objects as input and return the chunks as output with preserved metadata. This is ideal for RAG. 
        chunks = text_splitter.split_documents(document_list)

        # return embeddings 
        return chunks     


if __name__ == "__main__":
    json_path = Path(__file__).resolve().parent / "jsondump" / "result.json"

    with open(json_path, "r") as file:
        jsonData = json.load(file)

    chunker = textSplitter(jsonData)

    documents_chunks = chunker.chunksFromJson()
    print(f"Loaded {len(documents_chunks)} document objects")
