import uuid
import hashlib

def issue_vdc_mandate(spending_cap: float, currency: str, vendor: str) -> dict:
    """Issue a cryptographically signed Verifiable Digital Credential (VDC) mandate via AP2.
    
    Args:
        spending_cap: The maximum approved spending cap for this transaction.
        currency: The currency of the transaction (e.g., 'USD').
        vendor: The authorized vendor.
        
    Returns:
        A dictionary representing the signed payment mandate.
    """
    mandate_id = f"MND-AP2-{uuid.uuid4().hex[:6].upper()}"
    
    # Simulate a cryptographic signature over the payload
    payload = f"{mandate_id}:{spending_cap}:{currency}:{vendor}"
    signature = "sig:0x" + hashlib.sha256(payload.encode()).hexdigest()[:16]
    
    print(f"[AP2 Execution] Issued VDC Mandate {mandate_id} for {vendor} (Cap: ${spending_cap})")
    
    return {
        "mandate_status": "GENERATED_AND_SIGNED",
        "mandate_id": mandate_id,
        "spending_cap": spending_cap,
        "currency": currency,
        "cryptographic_proof": signature
    }
