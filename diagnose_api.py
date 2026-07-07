"""
Quick diagnostic: Check if we should use Vertex AI vs AI Studio for Gemini.

The current code uses google.generativeai (AI Studio SDK).
If the API key is actually for Vertex AI, we need different code.
"""

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GOOGLE_GENAI_API_KEY", "")
project = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
location = os.environ.get("GOOGLE_CLOUD_LOCATION", "")

print("=" * 60)
print("GEMINI API CONFIGURATION CHECK")
print("=" * 60)
print()
print(f"API Key: {api_key[:30]}..." if api_key else "❌ NO API KEY")
print(f"GCP Project: {project}")
print(f"GCP Location: {location}")
print()
print("=" * 60)
print()

if api_key.startswith("AIza"):
    print("✓ API Key format: AI Studio (google.generativeai)")
    print("  → Use: genai.GenerativeModel('gemini-pro-vision')")
elif api_key.startswith("AQ."):
    print("⚠ API Key format: Possibly OAuth/Service Account")
    print("  → Consider using Vertex AI SDK instead:")
    print("  → from vertexai.generative_models import GenerativeModel")
    print("  → model = GenerativeModel('gemini-1.5-flash')")
else:
    print("⚠ Unknown API key format")
    print(f"  → Starts with: {api_key[:5]}")

print()
print("=" * 60)
print("RECOMMENDED ACTION:")
print("=" * 60)

if project and location:
    print("You have GCP project + location configured.")
    print("→ TRY VERTEX AI instead of AI Studio")
    print()
    print("Update extractor.py to use:")
    print("  from vertexai.generative_models import GenerativeModel")
    print("  model = GenerativeModel('gemini-1.5-flash')")
else:
    print("Get a valid AI Studio API key from:")
    print("→ https://makersuite.google.com/app/apikey")
    print("  (Should start with 'AIza')")
