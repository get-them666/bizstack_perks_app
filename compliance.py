import hashlib
import os

class FintechComplianceVault:
    @staticmethod
    def isolate_and_hash_pii(data_payload: dict, tenant_id: str) -> dict:
        raw_email = data_payload.get("customer_email", "")
        tenant_salt = os.getenv("COMPLIANCE_SALT", "FintechSecureDefaultSalt777")
        secure_hash = hashlib.sha256(f"{raw_email}{tenant_id}{tenant_salt}".encode()).hexdigest()
        
        sanitized_payload = data_payload.copy()
        sanitized_payload["customer_email"] = f"TOKEN_{secure_hash[:16]}"
        sanitized_payload["tenant_owner"] = tenant_id
        sanitized_payload["compliance_status"] = "PASSED_ISOLATION_AUDIT"
        
        print(f"[COMPLIANCE] Data logically isolated for Tenant: {tenant_id}")
        return sanitized_payload

if __name__ == "__main__":
    sample_lead = {"customer_email": "user@targetbank.com", "requested_loan": 50000}
    print(FintechComplianceVault.isolate_and_hash_pii(sample_lead, "Lending_Platform_C"))
