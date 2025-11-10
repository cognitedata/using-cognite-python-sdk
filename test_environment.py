# Test script to verify Cognite SDK installation
import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    from cognite.client.credentials import OAuthInteractive
    from cognite.client import CogniteClient, ClientConfig
    print("✅ Cognite SDK imported successfully!")
    
    # Configuration
    TENANT_ID = "48d5043c-cf70-4c49-881c-c638f5796997"
    CLIENT_ID = "fab52bb5-9de2-4f9e-aefa-712da4b5fe00"
    CDF_CLUSTER = "westeurope-1"
    COGNITE_PROJECT = "ds-basics"
    BASE_URL = f"https://{CDF_CLUSTER}.cognitedata.com"
    
    print("✅ Configuration variables set successfully!")
    print(f"Base URL: {BASE_URL}")
    print(f"Project: {COGNITE_PROJECT}")
    
except ImportError as e:
    print(f"❌ Error importing Cognite SDK: {e}")
except Exception as e:
    print(f"❌ Error: {e}")