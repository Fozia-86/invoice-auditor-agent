import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Environment variables load karein
load_dotenv()

# Client initialize karein
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def audit_invoice(image_path: str):
    print(f"⌛ Analyzing invoice: {image_path}...")
    
    # 1. Image file ko open aur load karein
    with open(image_path, "rb") as f:
        image_bytes = f.read()
        
    # 2. Gemini ke liye image part tayar karein
    invoice_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/jpeg" # Agar PNG hai to "image/png" likhein
    )
    
    # 3. Strict Auditing Prompt definition
    audit_prompt = """
    You are an expert Forensic Accountant and Invoice Auditor. 
    Analyze the attached invoice image carefully and perform a strict audit based on these rules:
    
    1. Verify Calculations: Check if (Quantity * Unit Price) matches the Line Total for every item.
    2. Check Subtotal & Tax: Verify if the sum of line totals matches the Subtotal, and tax percentage is calculated correctly.
    3. Grand Total Check: Ensure Subtotal + Tax/Fees equals the Grand Total.
    4. Compliance Check: Identify if critical info is missing (Invoice Number, Date, Vendor Name, Client Name).
    5. Due Date Check: Highlight if the due date has already passed compared to today.
    
    Output Format:
    ## 📋 Invoice Audit Summary
    - **Vendor Name:** [Name]
    - **Invoice Number:** [Number]
    - **Total Amount:** [Amount]
    
    ## 🔍 Audit Findings
    - **Mathematical Accuracy:** [Pass/Fail with brief reason]
    - **Data Completeness:** [Pass/Fail - List missing fields if any]
    
    ## ⚠️ Flagged Issues / Anomalies
    - [List any calculation errors, missing taxes, or suspicious items here. If none, write "None"]
    
    ## 🎯 Final Recommendation
    - [Approve / Reject / Needs Manual Review]
    """
    
    # 4. Multi-modal call (Image + Prompt)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[invoice_part, audit_prompt]
    )
    
    return response.text

# --- Execution Area ---
if __name__ == "__main__":
    # Test invoice ka path badal kar is receipt ka naam likhein
    test_invoice_path = "hospital_receipt.jpg" 
    
    if os.path.exists(test_invoice_path):
        audit_report = audit_invoice(test_invoice_path)
        print("\n" + "="*40 + "\n")
        print(audit_report)
        print("\n" + "="*40 + "\n")
    else:
        print(f"❌ Error: Please place your receipt named '{test_invoice_path}' in this folder.")
