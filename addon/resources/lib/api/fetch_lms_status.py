import requests
import json
import xbmc
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.log_message import log_message
from resources.lib.utils.error_handling import log_exception
from resources.lib.utils.network_utils import create_requests_session, is_port_open, log_network_issue
from resources.lib.utils.constants import (
    LMS_SERVER_KEY,
    LMS_PORT_KEY,
    LMS_PLAYER_ID_KEY,
    LOG_LEVEL_INFO,
    JSON_RPC_URL_TEMPLATE,
    JSON_RPC_PAYLOAD_TEMPLATE,
    CONTENT_TYPE_HEADER
)

# Create a global session object with retry logic
requests_session = create_requests_session()

def fetch_lms_status():
    """
    Fetch the JSON data from the Logitech Media Server (LMS) using JSON-RPC.

    This function makes an HTTP POST request to the LMS to retrieve the current data.
    It handles potential errors and logs the response to the Kodi log.

    Returns:
        dict: A dictionary containing the JSON response data.
    """
    settings = read_settings()
    if not is_port_open(settings[LMS_SERVER_KEY], int(settings[LMS_PORT_KEY])):
        log_network_issue("LMS server port is not open.")
        return None

    url = construct_url(settings)
    payload = construct_payload(settings[LMS_PLAYER_ID_KEY])

    try:
        response = send_request(url, payload)
        data = parse_response(response)
        log_message("New 'now playing' received", LOG_LEVEL_INFO)
        return data
    except (requests.RequestException, KeyError, IndexError) as e:
        log_network_issue(f"Failed to fetch LMS status: {e}")
        log_exception(e)
        return None

def construct_url(settings):
    """
    Construct the URL for the JSON-RPC request.

    Args:
        settings (dict): The settings dictionary containing LMS server details.

    Returns:
        str: The constructed URL.
    """
    return JSON_RPC_URL_TEMPLATE.format(server=settings[LMS_SERVER_KEY], port=settings[LMS_PORT_KEY])

def construct_payload(player_id):
    """
    Construct the payload for the JSON-RPC request.

    Args:
        player_id (str): The LMS player ID.

    Returns:
        dict: The JSON-RPC payload.
    """
    payload = JSON_RPC_PAYLOAD_TEMPLATE.copy()
    payload["params"] = [player_id, ["status", "-", 10, "tags:adKl"]]
    return payload

def send_request(url, payload):
    """
    Send the HTTP POST request to the LMS.

    Args:
        url (str): The URL for the request.
        payload (dict): The JSON-RPC payload.

    Returns:
        requests.Response: The response from the server.
    """
    response = requests_session.post(url, json=payload, headers=CONTENT_TYPE_HEADER)
    response.raise_for_status()
    return response

def parse_response(response):
    """
    Parse the JSON response from the server.

    Args:
        response (requests.Response): The response from the server.

    Returns:
        dict: The parsed JSON data.
    """
    return response.json()

def log_beautified_json(data):
    """
    Log the beautified JSON response data.

    Args:
        data (dict): The JSON response data.
    """
    beautified_json = json.dumps(data, indent=4)
    log_message(f"Full JSON response:\n{beautified_json}", LOG_LEVEL_INFO)

