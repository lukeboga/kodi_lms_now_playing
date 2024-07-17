import requests
import xbmc
import json
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.log_message import log_message
from resources.lib.utils.error_handling import log_exception

# Create a global session object
requests_session = requests.Session()

def fetch_lms_status():
    """
    Fetch the JSON data from the Logitech Media Server (LMS) using JSON-RPC.
    
    This function makes an HTTP POST request to the LMS to retrieve the current data.
    It handles potential errors and logs the response to the Kodi log.
    
    Returns:
        dict: A dictionary containing the JSON response data.
    """
    settings = read_settings()
    url = f"http://{settings['lms_server']}:{settings['lms_port']}/jsonrpc.js"
    payload = {
        "method": "slim.request",
        "params": [settings['lms_player_id'], ["status", "-", 10, "tags:adKl"]],
        "id": 1
    }

    try:
        response = requests_session.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        data = response.json()

        # Log the entire JSON response (beautified with indentation)
        beautified_json = json.dumps(data, indent=4)
        log_message(f"Full JSON response:\n{beautified_json}", xbmc.LOGINFO)

        return data
    except requests.RequestException as e:
        log_message(f"Error fetching data: {e}", xbmc.LOGERROR)
        log_exception(e)
        return None
    except (KeyError, IndexError) as e:
        log_message(f"Error processing data: {e}", xbmc.LOGERROR)
        log_exception(e)
        return None

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `requests`: For making HTTP requests.
   - `xbmc`: Part of the Kodi API, used for logging.
   - `json`: For handling JSON data.
   - `read_settings`, `log_message`, `log_exception`: Custom utility functions for reading settings, logging messages, and logging exceptions.

2. **Global Session Object:**
   - `requests_session`: A global session object for making HTTP requests. This helps reuse the connection and improve performance.

3. **fetch_lms_status Function:**
   - **Purpose:** Fetch JSON data from the Logitech Media Server (LMS) using JSON-RPC.
   
   - **Returns:**
     - `dict`: A dictionary containing the JSON response data.
   
   - **Steps:**
     - Retrieves LMS settings using `read_settings`.
     - Constructs the URL and payload for the JSON-RPC request.
     - Makes the HTTP POST request using the global session object.
     - Parses the JSON response and logs it in a beautified format.
     - Handles and logs any exceptions that occur during the request or data processing.
   
   - **Detailed Steps:**
     - `settings = read_settings()`: Retrieves LMS settings.
     - `url = f"http://{settings['lms_server']}:{settings['lms_port']}/jsonrpc.js"`: Constructs the URL for the request.
     - `payload`: Constructs the JSON-RPC payload.
     - `response = requests_session.post(url, json=payload, headers={"Content-Type": "application/json"})`: Makes the HTTP POST request.
     - `data = response.json()`: Parses the JSON response.
     - `beautified_json = json.dumps(data, indent=4)`: Beautifies the JSON response for logging.
     - `log_message(f"Full JSON response:\n{beautified_json}", xbmc.LOGINFO)`: Logs the beautified JSON response.
     - `log_exception(e)`: Logs the exception and its traceback.
"""

