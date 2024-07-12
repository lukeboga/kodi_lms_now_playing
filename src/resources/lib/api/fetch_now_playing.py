import requests
import xbmc
from ..utils.log_message import log_message

LMS_URL = "http://192.168.1.201:9000/jsonrpc.js"
PLAYER_ID = "ab:7a:56:8b:fd:0f"
PAYLOAD = {
    "id": 1,
    "method": "slim.request",
    "params": [PLAYER_ID, ["status", "-"]]
}

def get_now_playing():
    """
    Fetch the current 'now playing' information from the LMS server.
    
    Returns:
        dict: Parsed JSON data from the LMS server containing 'now playing' information.
    """
    try:
        # Send a POST request to the LMS server
        response = requests.post(LMS_URL, json=PAYLOAD)
        # Parse the JSON response
        data = response.json()
        # Log the entire raw JSON response for debugging
        log_message(f"Raw Now Playing Data: {data}", xbmc.LOGDEBUG)
        
        # Extract relevant data for 'now playing' information
        result = data.get("result", {})
        if "playlist_loop" in result and len(result["playlist_loop"]) > 0:
            now_playing = {
                "title": result["playlist_loop"][0].get("title", "Unknown Title"),
                "artist": result.get("remoteMeta", {}).get("title", "Unknown Artist"),
                "album": result.get("current_title", "Unknown Album"),
                "time": result.get("time", 0)
            }
            # Format the extracted 'now playing' data for readable logging
            formatted_now_playing = (
                f"Now Playing Information:\n"
                f"Title: {now_playing['title']}\n"
                f"Artist: {now_playing['artist']}\n"
                f"Album: {now_playing['album']}\n"
                f"Time: {now_playing['time']}\n"
            )
            # Log the formatted 'now playing' data for debugging
            log_message(formatted_now_playing, xbmc.LOGDEBUG)
            return now_playing
        else:
            log_message("No playlist_loop data available.", xbmc.LOGWARNING)
            return None
    except Exception as e:
        log_message(f"Error fetching now playing: {e}", xbmc.LOGERROR)
        return None

