# Test script to verify Cognite SDK installation
import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    from cognite.client.credentials import OAuthInteractive
    from cognite.client import CogniteClient, ClientConfig
    print("✅ Cognite SDK imported successfully!")
    
    # Configuration
    TENANT_ID = "24df34ab-a358-4b62-ba14-e5dfb43b9d63"
    CLIENT_ID = "22352de2-1f0f-48a0-ab9a-de17bbd48675"
    CDF_CLUSTER = "aw-was-gp-001"
    COGNITE_PROJECT = "oxy-oog-dev"
    BASE_URL = f"https://{CDF_CLUSTER}.cognitedata.com"
    
    print("✅ Configuration variables set successfully!")
    print(f"Base URL: {BASE_URL}")
    print(f"Project: {COGNITE_PROJECT}")
    
except ImportError as e:
    print(f"❌ Error importing Cognite SDK: {e}")
except Exception as e:
    print(f"❌ Error: {e}")