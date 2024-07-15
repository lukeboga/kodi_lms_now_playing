import requests
import xbmc
import json
from resources.lib.utils.read_settings import read_settings

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
    # Retrieve LMS settings
    settings = read_settings()
    url = f"http://{settings['lms_server']}:{settings['lms_port']}/jsonrpc.js"
    payload = {
        "method": "slim.request",
        "params": [settings['lms_player_id'], ["status", "-", 10, "tags:adKl"]],
        "id": 1
    }

    try:
        # Make the API request to the LMS
        response = requests_session.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()  # Parse the JSON response

        # Log the entire JSON response (beautified with indentation)
        beautified_json = json.dumps(data, indent=4)
        xbmc.log(f"Full JSON response:\n{beautified_json}", level=xbmc.LOGINFO)

        return data
    except requests.RequestException as e:
        # Log any errors encountered during the API request
        xbmc.log(f"Error fetching data: {e}", level=xbmc.LOGERROR)
        return None
    except (KeyError, IndexError) as e:
        # Log any errors encountered during data extraction
        xbmc.log(f"Error processing data: {e}", level=xbmc.LOGERROR)
        return None

