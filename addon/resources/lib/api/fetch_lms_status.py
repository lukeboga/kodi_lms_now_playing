import json
import xbmc
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.log_message import log_message
from resources.lib.utils.error_handling import log_exception
from resources.lib.utils.network_utils import create_requests_session, is_port_open, log_network_issue

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
    if not is_port_open(settings['lms_server'], int(settings['lms_port'])):
        log_network_issue("LMS server port is not open.")
        return None

    url = construct_url(settings)
    payload = construct_payload(settings['lms_player_id'])

    try:
        response = send_request(url, payload)
        data = parse_response(response)
        log_beautified_json(data)
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
    return f"http://{settings['lms_server']}:{settings['lms_port']}/jsonrpc.js"

def construct_payload(player_id):
    """
    Construct the payload for the JSON-RPC request.

    Args:
        player_id (str): The LMS player ID.

    Returns:
        dict: The JSON-RPC payload.
    """
    return {
        "method": "slim.request",
        "params": [player_id, ["status", "-", 10, "tags:adKl"]],
        "id": 1
    }

def send_request(url, payload):
    """
    Send the HTTP POST request to the LMS.

    Args:
        url (str): The URL for the request.
        payload (dict): The JSON-RPC payload.

    Returns:
        requests.Response: The response from the server.
    """
    response = requests_session.post(url, json=payload, headers={"Content-Type": "application/json"})
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
    log_message(f"Full JSON response:\n{beautified_json}", xbmc.LOGINFO)

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `json`: For handling JSON data.
   - `xbmc`: Part of the Kodi API, used for logging.
   - `read_settings`, `log_message`, `log_exception`: Custom utility functions for reading settings, logging messages, and logging exceptions.
   - `create_requests_session`, `is_port_open`, `log_network_issue`: Custom network utility functions for creating a requests session, checking if a port is open, and logging network issues.

2. **Global Session Object:**
   - `requests_session`: A global session object for making HTTP requests with retry logic. This helps reuse the connection and improve performance.

3. **fetch_lms_status Function:**
   - **Purpose:** Fetch JSON data from the Logitech Media Server (LMS) using JSON-RPC.
   - **Returns:** `dict`: A dictionary containing the JSON response data.
   - **Steps:**
     - Retrieves LMS settings using `read_settings`.
     - Checks if the LMS server port is open using `is_port_open`.
     - Constructs the URL and payload for the JSON-RPC request.
     - Makes the HTTP POST request using the global session object.
     - Parses the JSON response and logs it in a beautified format.
     - Handles and logs any exceptions that occur during the request or data processing using `log_network_issue` and `log_exception`.

4. **Helper Functions:**
   - **construct_url:** Constructs the URL for the JSON-RPC request using LMS settings.
   - **construct_payload:** Constructs the JSON-RPC payload using the LMS player ID.
   - **send_request:** Sends the HTTP POST request and raises any status errors.
   - **parse_response:** Parses the JSON response from the server.
   - **log_beautified_json:** Logs the beautified JSON response data.

"""

