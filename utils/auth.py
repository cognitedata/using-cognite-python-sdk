# Copyright 2022 Cognite AS
import os
from pathlib import Path

from cognite.client import ClientConfig, CogniteClient
from cognite.client.credentials import OAuthClientCredentials, Token
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

BASE_URL = f"https://{CDF_CLUSTER}.cognitedata.com"
SCOPES = [f"https://{CDF_CLUSTER}.cognitedata.com/.default"]

AUTHORITY_HOST_URI = "https://login.microsoftonline.com"
AUTHORITY_URI = AUTHORITY_HOST_URI + "/" + TENANT_ID
PORT = 53000

TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"


def interactive_client():
    """Function to Create the Cognite Client, using Interactive Login method"""
    app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY_URI)
    creds = app.acquire_token_interactive(scopes=SCOPES, port=PORT)
    cnf = ClientConfig(
        client_name="my-special-client",
        project=COGNITE_PROJECT,
        credentials=Token(creds["access_token"]),
        base_url=BASE_URL,
    )
    client = CogniteClient(cnf)
    return client


def device_code_client():
    """Function to Create the Cognite Client, using Device code method"""
    app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY_URI)
    device_flow = app.initiate_device_flow(scopes=SCOPES)
    print(device_flow["message"])  # print device code to screen
    creds = app.acquire_token_by_device_flow(flow=device_flow)
    cnf = ClientConfig(
        client_name="my-special-client",
        project=COGNITE_PROJECT,
        credentials=Token(creds["access_token"]),
        base_url=BASE_URL,
    )
    client = CogniteClient(cnf)
    return client


def client_secret_client():
    """Function to Create the Cognite Client, using Credentials (e.g. ClientID, Client secret)"""
    creds = OAuthClientCredentials(
        token_url=TOKEN_URL,
        client_id=CLIENT_ID,
        scopes=SCOPES,
        client_secret=CLIENT_SECRET,
    )
    cnf = ClientConfig(
        client_name="my-special-client",
        project=COGNITE_PROJECT,
        credentials=creds,
        base_url=BASE_URL,
    )
    client = CogniteClient(cnf)
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
