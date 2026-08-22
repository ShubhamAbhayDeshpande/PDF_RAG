from langchain_huggingface import HuggingFaceEmbeddings

EMBEDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

class retriever: 
    def __init__(self): 
        self.embedding_model=HuggingFaceEmbeddings(
                    model_name=EMBEDING_MODEL,
                    encode_kwargs={"normalize_embeddings": True},
                    )

    def query_embedding(self, query_text: str) -> list: 
        """
        Method used for embedding user query. Returns list of query embeddings. 
        
        return: list
        
        """
    
        query_embedding = self.embedding_model.embed_query(query_text)

        return query_embedding
        
        