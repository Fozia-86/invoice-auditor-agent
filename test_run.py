import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agent import process_invoice

print("Running manual test...")
result = process_invoice("gs://invoice-auditor-agent-bucket/raw/invoice.pdf")
print("\n--- FINAL OUTPUT ---")
print(result)
