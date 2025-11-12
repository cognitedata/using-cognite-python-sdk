# Test script to verify Cognite SDK installation
import sys
from pathlib import Path

# Add utils to path to import customer configs
sys.path.insert(0, str(Path(__file__).parent / "utils"))

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    from cognite.client.credentials import OAuthInteractive
    from cognite.client import CogniteClient, ClientConfig
    from cognite_auth import CUSTOMER_CONFIGS  # type: ignore
    print("✅ Cognite SDK imported successfully!")
    
    # Test with a customer (default to "oxy" if not specified)
    customer = sys.argv[1] if len(sys.argv) > 1 else "oxy"
    
    if customer not in CUSTOMER_CONFIGS:
        print(f"❌ Customer '{customer}' not found. Available customers: {list(CUSTOMER_CONFIGS.keys())}")
        sys.exit(1)
    
    # Get configuration for customer
    config = CUSTOMER_CONFIGS[customer]
    tenant_id = config["tenant_id"]
    client_id = config["client_id"]
    cdf_cluster = config["cdf_cluster"]
    cognite_project = config["cognite_project"]
    base_url = f"https://{cdf_cluster}.cognitedata.com"
    
    print("✅ Configuration variables set successfully!")
    print(f"Customer: {customer}")
    print(f"Base URL: {base_url}")
    print(f"Project: {cognite_project}")
    print(f"Tenant ID: {tenant_id}")
    print(f"Client ID: {client_id}")
    
except ImportError as e:
    print(f"❌ Error importing Cognite SDK: {e}")
except Exception as e:
    print(f"❌ Error: {e}")