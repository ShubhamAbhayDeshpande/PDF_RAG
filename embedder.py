"""
This python module will generate embeddings from the chunks of texts in that are provided as inputs. 

The embeddings will be purely text embeddings. The images will be treated as metadata and when the recall is made by RAG, the 
images will be called and shown in the citation. 

For the embeddings, LangChain-Hugging face embedding model is used which runs locally. The model used is all-MiniLM-L6-v2. 

"""
# Imports
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
import os

# Constants
CHORMA_DB_PATH="chroma_db/"
EMBEDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME="pdfDocs"


class embedder:
    def __init__(self, chunks):
        self.chunks = chunks
        self.document_embedding=[]
        self.ids_list=[]

        # Importing model
        self.embedding_model=HuggingFaceEmbeddings(
            model_name=EMBEDING_MODEL,
            encode_kwargs={"normalize_embeddings": True},
            )

        # List of all the text and metadata associated with the text
        self._documentTextLilst = [chunk.page_content for chunk in self.chunks]
        self.metadataList = [chunk.metadata for chunk in self.chunks]

        # TEMP CODE: Check if the db with this name already exists in the folder. If yes, delete it. 
        for fname in os.listdir(r"chroma_db"):
            if fname.endswith("sqlite3"):
                os.remove(os.path.join("chroma_db", fname))

        

    def embedding_and_database(self) -> list:
        """
        This method will take the cunks from the langchain generator as inputs and will produce the chunks using 'all-MiniLM-L6-v2' as embeddings model. 
        """
        # .embed_documents() is a method used for making the vectors for the source documents in a RAG. 
        # The ids we just need for the chromadb
        for ids , _ in enumerate(self._documentTextLilst):
            self.ids_list.append(f"id{ids}")
        self.document_embedding = self.embedding_model.embed_documents(self._documentTextLilst)

       # Make vector database
       # Make a local chromadb server to store the vector data later on. 
        client = chromadb.PersistentClient(path=r"chroma_db") # Persistent Client to store the data. 
       
        # Collections are fundamental units for managing vector database and running queries in the database. 
        collection = client.create_collection(name="pdf_collection")

        # Add data into the collection
        collection.add(
            ids=self.ids_list,
            embeddings=self.document_embedding,
            metadatas=self.metadataList
        )

    def query_embedding(self, query_text: str) -> list:
        """
        Method used for embedding user query. Returns list of query embeddings. 
        
        return: list
        
        """

        query_embedding = self.embedding_model.embed_query(query_text)

        return query_embedding


