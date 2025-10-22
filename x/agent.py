import hashlib
import json
import os
from typing import List

import httpx
from google.adk.agents.llm_agent import Agent
from google.adk.tools.openapi_tool import OpenAPIToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import \
    token_to_scheme_credential


def find_exit_by_hash(possible_exits: List[str], hash_start: str) -> str:
    """Finds an exit name from the list of possible exits whose SHA-256 hash starts
    with the given hash_start.
    Args:
        possible_exits (List[str]): A list of possible exit names.
        hash_start (str): The starting string of the SHA-256 hash to match.
    Returns:
        str: The exit name whose SHA-256 hash starts with hash_start, or an error
        message if no such exit is found.
    """
    if not hash_start:
        return "I'm sorry, but you must provide a hash_start."
    for exit_name in possible_exits:
        sha256 = hashlib.sha256(exit_name.encode()).hexdigest()
        if sha256.startswith(hash_start):
            return exit_name
    return (
        "I'm sorry, none of the hashes of the exits you provided have a prefix "
        "matching the hash_start you gave me"
    )


def fetch_url(url: str) -> str:
    """Fetches the content of a URL.
    Args:
        url (str): The URL to fetch.
    Returns:
        str: The content of the URL.
    """
    with httpx.Client(follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text


def get_schema() -> str:
    """Fetches the OpenAPI schema from the remote server.
    Returns:
        dict: The OpenAPI schema.
    """
    with httpx.Client() as client:
        openapi_spec = client.get("https://adventure.wietsevenema.eu/openapi.json").json()
    return json.dumps(openapi_spec) # Wont work to return response.text



openapi_spec = get_schema()

auth_scheme, auth_credential = token_to_scheme_credential(
    "apikey",
    "header",
    "Authorization",
    f"ApiKey {os.environ.get('ADK_API_KEY')}",
)

adventure_game_toolset = OpenAPIToolset(
    spec_str=openapi_spec,
    spec_str_type="json",
    auth_scheme=auth_scheme,
    auth_credential=auth_credential,
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="An expert adventure game player.",
    instruction=("""You are an expert adventure game player. Use the provided tools to \n
        interact with the adventure game world and achieve your objectives.\n"""
    ),
    tools=[adventure_game_toolset, fetch_url, find_exit_by_hash],
)
