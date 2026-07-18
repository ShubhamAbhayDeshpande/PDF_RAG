'''
The file responsible for generating the content from the model

'''
# Imports
import json
import os
from dotenv import load_dotenv
from google import genai

class LLMAPI:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("No API key found in .env file.")
        
        self.client = genai.client(api_key=api_key)

    # Using embeddings
    

