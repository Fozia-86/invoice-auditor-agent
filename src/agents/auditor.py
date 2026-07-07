import json
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from src.tools.mcp_server import get_company_policy
from src.tools.ucp_commerce import verify_vendor_checkout
from src.tools.ap2_payment import issue_vdc_mandate

def audit_and_execute(invoice_json_str: str) -> str:
    """Audit the extracted invoice data and execute payment if compliant.
    
    Args:
        invoice_json_str: The JSON string containing the extracted invoice data.
        
    Returns:
        A JSON string representing the transaction lifecycle audit verdict.
    """
    try:
        invoice_data = json.loads(invoice_json_str)
        vendor = invoice_data.get("vendor", "Unknown")
        category = invoice_data.get("category", "general")
        total = invoice_data.get("total_amount_usd", 0.0)
        
        # 1. Fetch Policy (MCP)
        policy = get_company_policy(category)
        max_limit = policy.get("max_limit_usd", 0.0)
        
        # 2. Audit compliance
        if total > max_limit:
            return json.dumps({"status": "REJECTED", "reason": f"Exceeds max limit of {max_limit}"})
            
        # 3. Vendor verification (UCP)
        session_id = f"ucp_session_{vendor.lower()[:3]}9941a"
        ucp_check = verify_vendor_checkout(session_id, vendor, total)
        
        if ucp_check.get("status") != "VERIFIED_MATCH":
            return json.dumps({"status": "REJECTED", "reason": "Vendor validation failed."})
            
        # 4. AP2 Payment Execution
        ap2_execution = issue_vdc_mandate(total, "USD", vendor)
        
        return json.dumps({
            "status": "APPROVED",
            "mcp_context_used": "company_policy.json",
            "flags_raised": 0,
            "ucp_handshake": ucp_check,
            "ap2_execution": ap2_execution
        })
        
    except Exception as e:
        return json.dumps({"status": "ERROR", "reason": str(e)})

auditor_agent = Agent(
    name="compliance_auditor",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""You are the Compliance Auditor Agent. You receive extracted invoice data JSON.
    Your job is to run the audit_and_execute tool on this data to ensure it meets company policy, 
    verifies with UCP, and issues an AP2 mandate. Return the final structured lifecycle JSON.""",
    tools=[audit_and_execute]
)
