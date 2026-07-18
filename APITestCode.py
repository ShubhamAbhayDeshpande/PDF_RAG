import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

MODEL_ID = "gemini-2.5-flash"
SYSTEM_INSTRUCTIONS = "You are the genie from the aladdin movie played by Robin Williams. Explain everything like the genie" \
                        "would explain it." 


load_dotenv()

try:
    API_KEY = os.getenv("GEMINI_API_KEY")
except Exception:
    print("API KEY FAILURE")
    API_KEY = None

client = genai.Client(api_key=API_KEY)

interaction = client.interactions.create(
    model=MODEL_ID, 
    input="Explain how AI works in few words",
    system_instruction=SYSTEM_INSTRUCTIONS,
)

print(f"Number of steps: {len(interaction.steps)}")
for j, step in enumerate(interaction.steps):
    print(f"step{j}: type={step.type}")
