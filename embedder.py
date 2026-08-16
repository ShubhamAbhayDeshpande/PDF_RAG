"""
This python module will generate embeddings from the chunks of texts in that are provided as inputs. 

The embeddings will be purely text embeddings. The images will be treated as metadata and when the recall is made by RAG, the 
images will be called and shown in the citation. 

For the embeddings, LangChain-Hugging face embedding model is used which runs locally. The model used is all-MiniLM-L6-v2. 

"""
# Imports
from langchain_huggingface import HuggingFaceEmbeddings

class embedder:
    def __init__(self, chunks):
        self.chunks = chunks

        # Importing model
        self.embedding_model=HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            encode_kwargs={"normalize_embeddings": True},
            )

        # List of all the text 
        self._documentTextLilst = [chunk.page_content for chunk in self.chunks]

        

    def embedding_generator(self) -> list:
        """
        This method will take the cunks from the langchain generator as inputs and will produce the chunks using 'all-MiniLM-L6-v2' as embeddings model. 
        """
        query_list = [self.embedding_model.embed_query(text) for text in self._documentTextLilst]
        return query_list
        

        
        
        

        
        
