# Copyright 2022 Cognite AS
import os
from pathlib import Path

from cognite.client import CogniteClient
from dotenv import load_dotenv
from msal import PublicClientApplication

# These values can also be set via config files
TENANT_ID = "48d5043c-cf70-4c49-881c-c638f5796997"
CLIENT_ID = "fab52bb5-9de2-4f9e-aefa-712da4b5fe00"
CDF_CLUSTER = "westeurope-1"
COGNITE_PROJECT = "ds-basics"

# Obtain the Environment Variables from .env file
dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)
CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # store secret in .env file

SCOPES = [f"https://{CDF_CLUSTER}.cognitedata.com/.default"]

AUTHORITY_HOST_URI = "https://login.microsoftonline.com"
AUTHORITY_URI = AUTHORITY_HOST_URI + "/" + TENANT_ID
PORT = 53000

TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"


def interactive_client():
    """Function to Create the Cognite Client, using Interactive Login method"""
    app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY_URI)
    creds = app.acquire_token_interactive(scopes=SCOPES, port=PORT)
    client = CogniteClient(
        token_url=creds["id_token_claims"]["iss"],
        token=creds["access_token"],
        token_client_id=creds["id_token_claims"]["aud"],
        project=COGNITE_PROJECT,
        base_url=f"https://{CDF_CLUSTER}.cognitedata.com",
        client_name="cognite-client-interactive",
    )
    return client


def device_code_client():
    """Function to Create the Cognite Client, using Device code method"""
    app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY_URI)
    device_flow = app.initiate_device_flow(scopes=SCOPES)
    print(device_flow["message"])  # print device code to screen
    creds = app.acquire_token_by_device_flow(flow=device_flow)
    client = CogniteClient(
        token_url=creds["id_token_claims"]["iss"],
        token=creds["access_token"],
        token_client_id=creds["id_token_claims"]["aud"],
        project=COGNITE_PROJECT,
        base_url=f"https://{CDF_CLUSTER}.cognitedata.com",
        client_name="cognite-client-device",
    )
    return client


def client_secret_client():
    """Function to Create the Cognite Client, using Credentials (e.g. ClientID, Client secret)"""
    client = CogniteClient(
        token_url=TOKEN_URL,
        token_client_id=CLIENT_ID,
        token_client_secret=CLIENT_SECRET,
        token_scopes=SCOPES,
        project=COGNITE_PROJECT,
        base_url=f"https://{CDF_CLUSTER}.cognitedata.com",
        client_name="client_secret_test_script",
        debug=False,
    )
    return client


def create_cognite_client(method="interactive-login") -> CogniteClient:
    """Function to Create the Client
    Args:
        method (str, optional): One of the methods
        ("interactive-login","device-code","client-secret").
        Defaults to "interactive-login".

    Returns:
        CogniteClient: CogniteClient to be used to access Cognite Data Fusion.
    """
    if method == "interactive-login":
        client = interactive_client()
    elif method == "device-code":
        client = device_code_client()
    elif method == "client-secret":
        client = client_secret_client()
    else:
        client = None
        print(
            "Client couldn't be created. Methods : interactive-login, device-code, client-secret"
        )
    return client
