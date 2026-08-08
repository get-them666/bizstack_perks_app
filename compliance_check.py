import re

def verify_business_address(address_string):
    """
    Validates structure and ensures address parameters meet institutional underwriting criteria.
    """
    if not address_string or len(address_string.strip()) < 10:
        return False, "Address input is too short to verify."
        
    cleaned_address = address_string.upper().strip()
    
    # Flag invalid PO Box definitions
    po_box_patterns = [r"P\.?\s*O\.?\s*BOX", r"POST\s+OFFICE\s+BOX"]
    for pattern in po_box_patterns:
        if re.search(pattern, cleaned_address):
            return False, "PO Box addresses are ineligible for asset-backed commercial underwriting lines."
            
    # Ensure standard street type signatures exist
    valid_street_identifiers = ["ST", "STREET", "DR", "DRIVE", "RD", "ROAD", "AVE", "AVENUE", "BLVD", "BOULEVARD", "LN", "LANE", "CT", "COURT", "WAY", "PL", "PLACE"]
    has_street_type = any(re.search(rf"\b{ident}\b", cleaned_address) for ident in valid_street_identifiers)
    
    # Match basic structural layout (Starts with numeric sequence, ends with 5-digit zip identifier)
    has_numeric_start = bool(re.match(r"^\d+", cleaned_address))
    has_zip_code = bool(re.search(r"\b\d{5}(-\d{4})?\b", cleaned_address))
    
    if not (has_street_type and has_numeric_start and has_zip_code):
        return False, "Address missing critical street destination indicators or standard ZIP sequence."
        
    return True, "Address profile structurally confirmed for financial processing."

if __name__ == "__main__":
    # Test evaluation with your default commercial target address
    test_addr = "701 DANA DRIVE CHESAPEAKE, VA 23321"
    is_valid, msg = verify_business_address(test_addr)
    print(f"Address: {test_addr}\nStatus Verified: {is_valid} | Result Detail: {msg}")
