#!/usr/bin/env python3
"""Check which Gemini models are available with the current API key."""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API
api_key = os.environ.get("GOOGLE_GENAI_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_GENAI_API_KEY not found in environment")
    exit(1)

print(f"✓ API Key found: {api_key[:20]}...")
print()

try:
    genai.configure(api_key=api_key)
    print("Listing available models:")
    print("-" * 60)

    models = genai.list_models()

    for model in models:
        print(f"\nModel: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Description: {model.description[:100] if model.description else 'N/A'}...")
        print(f"  Supported Methods: {', '.join(model.supported_generation_methods)}")

        # Check if it supports generateContent (needed for multimodal)
        if 'generateContent' in model.supported_generation_methods:
            print(f"  ✓ SUPPORTS generateContent (good for invoice extraction)")

    print("\n" + "=" * 60)
    print("\nRECOMMENDED MODELS FOR INVOICE EXTRACTION:")
    print("-" * 60)

    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            # Extract just the model name without the 'models/' prefix
            model_name = model.name.replace('models/', '')
            print(f"  • {model_name}")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
