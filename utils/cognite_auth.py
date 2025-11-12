from pathlib import Path
from cognite.client import ClientConfig, CogniteClient
from cognite.client.credentials import OAuthInteractive

# Customer configurations
CUSTOMER_CONFIGS = {
    "oxy": {
        "tenant_id": "24df34ab-a358-4b62-ba14-e5dfb43b9d63",
        "client_id": "22352de2-1f0f-48a0-ab9a-de17bbd48675",
        "cdf_cluster": "aw-was-gp-001",
        "cognite_project": "oxy-oog-dev",
    },
    # Add more customer configurations here as needed
    # "customer2": {
    #     "tenant_id": "...",
    #     "client_id": "...",
    #     "cdf_cluster": "...",
    #     "cognite_project": "...",
    # },
}


def interactive_client(customer, token_cache_path=None):
    """
    Function to instantiate the CogniteClient, using the interactive auth flow.
    
    Args:
        customer: Customer name (must exist in CUSTOMER_CONFIGS)
        token_cache_path: Optional path to store token cache FILE (not directory). 
                         If None, uses in-memory cache (no persistent storage).
                         Example: Path.home() / ".cognite" / "token_cache.json"
                         MSAL will create a single file at this location.
    
    Returns:
        CogniteClient instance
    
    Raises:
        ValueError: If customer is not found in CUSTOMER_CONFIGS
    """
    if customer not in CUSTOMER_CONFIGS:
        raise ValueError(
            f"Customer '{customer}' not found. Available customers: {list(CUSTOMER_CONFIGS.keys())}"
        )
    
    config = CUSTOMER_CONFIGS[customer]
    tenant_id = config["tenant_id"]
    client_id = config["client_id"]
    cdf_cluster = config["cdf_cluster"]
    cognite_project = config["cognite_project"]
    base_url = f"https://{cdf_cluster}.cognitedata.com"
    
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
            project=cognite_project,
            base_url=base_url,
            credentials=OAuthInteractive(
                authority_url=f"https://login.microsoftonline.com/{tenant_id}",
                client_id=client_id,
                scopes=[f"{base_url}/.default"],
                token_cache_path=cache_path,
            ),
        )
    )
