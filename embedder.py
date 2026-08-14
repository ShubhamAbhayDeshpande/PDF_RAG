"""
This python module will generate embeddings from the chunks of texts in that are provided as inputs. 

The embeddings will be purely text embeddings. The images will be treated as metadata and when the recall is made by RAG, the 
images will be called and shown in the citation. 

For the embeddings, LangChain-Hugging face embedding model is used which runs locally. The model used is all-MiniLM-L6-v2. 

"""

from langchain_huggingface import HuggingFaceEmbeddings