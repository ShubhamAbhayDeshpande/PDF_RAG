'''
The file responsible for generating the content from the model

'''
# Imports
import json
import os
from dotenv import load_dotenv
from google import genai

# Constant
MODEL_ID = "gemini-2.5-flash"

class LLMAPI:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("No API key found in .env file.")
        
        self.client = genai.Client(api_key=api_key)

    # Using embeddings

    def generate_answer(self, question: str, context: str) -> str:
        """
        The method will accept the answer and the context as input and sent it to the LLM API. 
        The reply from the Gemini will be returned as an answer. 
        
        return: answer string
        """
        SYSTEM_INSTRUCTIONS = f"""
                        Use the information provided in the following context to answer the question by the user.: 
                    

                        CONTEXT: {context}

                        You are free to search the available resources on the internet or in your personal database along with the 
                        provided context. The important thing is that, provided context should be used in the final naswer. """

        interaction = self.client.interactions.create(
            model = MODEL_ID, 
            input= question, 
            system_instruction=SYSTEM_INSTRUCTIONS
        )

        return interaction.output_text



