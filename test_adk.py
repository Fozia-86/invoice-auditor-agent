import os
from google import genai
from dotenv import load_dotenv

# .env file se variables load karne ke liye
load_dotenv()

# Sahi environment variable (GEMINI_API_KEY) read karein
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Model badal kar "gemini-2.5-flash" ya "gemini-3.5-flash" karein
resp = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="hello"
)

print(resp.text)
