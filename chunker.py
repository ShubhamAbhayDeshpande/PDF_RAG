"""
The program will create chunks from the text and images in the pdf file. 

Creator: Shubham Deshpande
Version: 0.0

"""
# Imports
import json
from pathlib import Path
import fitz
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_core.documents import Document

class textSplitter:
    """
    This class will accept string object as an input and it will do the chunking for the text and return the 
    splitted text as output. 
    
    """
    def __init__(self, jsonObj, maxChunkSize=20, minChunkSize=100):
        self.jsonObj=jsonObj
        self.minChunkSize=minChunkSize
        self.maxChunkSize=maxChunkSize

    def documentObjFromJson(self)-> list:
        """
        This function will accept the json object created from the document as an input and it will output a document 
        object used in the text splitter later. 
        
        """
        # we can directly parse the document because I know the structure for the json object. 
        document_list = []

        for doc_num, document_name in enumerate(self.jsonObj.keys()):
             meta_data = dict()
             for pages_key in self.jsonObj[document_name].keys():

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
                meta_data["chunk_id"]="doc"+str(doc_num)+"_"+pages_key
                meta_data["image_ids"]=image_xrfs
                meta_data["image_paths"]=image_paths 

                document_list.append(
                    Document(page_content=page_data.get("text", ""), 
                             metadata=meta_data
                             )
                        )
        
                      
        return document_list
