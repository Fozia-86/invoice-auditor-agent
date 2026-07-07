import os
import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Environment variables load karein
load_dotenv()

class InvoiceAuditorAgent:
    def __init__(self):
        # API key automatic environment se mil jayegi
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"

    def audit_invoice(self, file_bytes: bytes, mime_type: str) -> str:
        """Core AI logic jo cloud runtime par chalega"""
        invoice_part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
        
        audit_prompt = """
        You are an expert Invoice Auditor. Analyze this invoice carefully.
        Provide the response in two clear sections:
        
        ---DATA_START---
        Vendor: [Only Vendor Name]
        InvoiceNumber: [Only Invoice/Lab Number]
        TotalAmount: [Only Numeric Value, e.g. 2200]
        Status: [Approved / Rejected / Flagged]
        ---DATA_END---
        
        ## 📋 Invoice Audit Summary
        Provide the visual markdown report here with Findings, Flagged Issues, and Final Recommendation.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[invoice_part, audit_prompt]
        )
        return response.text

# Live Agent Runtime Entrypoint Function
def start_agent():
    """Yeh function agent.toml ka entrypoint hai jise cloud call karega"""
    print("🚀 Smart Invoice Auditor Agent started successfully on Agent Runtime!")
    return InvoiceAuditorAgent()

if __name__ == "__main__":
    # Local verification block
    agent = start_agent()