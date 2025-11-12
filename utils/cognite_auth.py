from pathlib import Path
from cognite.client import ClientConfig, CogniteClient
from cognite.client.credentials import OAuthInteractive

TENANT_ID = "24df34ab-a358-4b62-ba14-e5dfb43b9d63"
CLIENT_ID = "22352de2-1f0f-48a0-ab9a-de17bbd48675"
CDF_CLUSTER = "aw-was-gp-001"
COGNITE_PROJECT = "oxy-oog-dev"
BASE_URL = f"https://{CDF_CLUSTER}.cognitedata.com"
SCOPES = [f"{BASE_URL}/.default"]


def interactive_client(token_cache_path=None):
    """
    Function to instantiate the CogniteClient, using the interactive auth flow.
    
    Args:
        token_cache_path: Optional path to store token cache FILE (not directory). 
                         If None, uses in-memory cache (no persistent storage).
                         Example: Path.home() / ".cognite" / "token_cache.json"
                         MSAL will create a single file at this location.
    
    Returns:
        CogniteClient instance
    """
    cache_path = token_cache_path or None
    if cache_path:
        # Ensure it's a Path object (SDK expects Path, not str)
        if not isinstance(cache_path, Path):
            cache_path = Path(cache_path)
        # Create parent directory if it doesn't exist (cache_path is a file)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        # Keep as Path object - SDK expects Path and calls .exists() on it
    
    return CogniteClient(
        ClientConfig(
            client_name="Cognite Academy course taker",
            project=COGNITE_PROJECT,
            base_url=BASE_URL,
            credentials=OAuthInteractive(
                authority_url=f"https://login.microsoftonline.com/{TENANT_ID}",
                client_id=CLIENT_ID,
                scopes=[f"{BASE_URL}/.default"],
                token_cache_path=cache_path,
            ),
        )
    )
