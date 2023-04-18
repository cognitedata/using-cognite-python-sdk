from cognite.client import ClientConfig, CogniteClient
from cognite.client.credentials import OAuthInteractive

TENANT_ID = "48d5043c-cf70-4c49-881c-c638f5796997"
CLIENT_ID = "fab52bb5-9de2-4f9e-aefa-712da4b5fe00"
CDF_CLUSTER = "westeurope-1"
COGNITE_PROJECT = "ds-basics"
BASE_URL = f"https://{CDF_CLUSTER}.cognitedata.com"
SCOPES = [f"{BASE_URL}/.default"]


def interactive_client():
    """Function to instantiate the CogniteClient, using the interactive auth flow"""
    return CogniteClient(
        ClientConfig(
            client_name="Cognite Academy course taker",
            project=COGNITE_PROJECT,
            base_url=BASE_URL,
            credentials=OAuthInteractive(
                authority_url=f"https://login.microsoftonline.com/{TENANT_ID}",
                client_id=CLIENT_ID,
                scopes=[f"{BASE_URL}/.default"],
            ),
        )
    )
