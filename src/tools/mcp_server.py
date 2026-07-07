import json
import os

def get_company_policy(category: str) -> dict:
    """Fetch the enterprise expense policy and spending limits for a given category via MCP.
    
    Args:
        category: The expense category to check (e.g., 'hardware', 'software', 'travel', 'general').
        
    Returns:
        A dictionary containing the max_limit_usd, requires_approval_above, and allowed_vendors.
    """
    # The config file is located in the top-level config directory
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
        "config", 
        "company_policy.json"
    )
    
    try:
        with open(config_path, "r") as f:
            policy_data = json.load(f)
            
        expense_policies = policy_data.get("expense_policies", {})
        if category in expense_policies:
            return expense_policies[category]
        else:
            return expense_policies.get("general", {})
            
    except Exception as e:
        return {"error": f"Failed to load policy: {str(e)}"}
