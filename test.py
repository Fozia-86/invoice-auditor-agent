import os
from google import genai

# 1. Direct environment variable se key read karein (jo abhi humne set ki)
api_key = os.environ.get("GEMINI_API_KEY")

# 2. Client ko initialize karte waqt key lazmi pass karein
client = genai.Client(api_key=api_key)

# 3. Apna model call karein
resp = client.models.generate_content(
    model='gemini-2.5-flash', # ya jo bhi model aap use kar rahi hain
    contents='Hello, tell me a joke.'
)

print(resp.text)
