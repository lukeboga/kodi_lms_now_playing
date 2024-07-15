import xbmc
from resources.lib.utils.log_message import log_message

def log_now_playing(data):
    """
    Log the 'now playing' data to the Kodi log in a readable format.
    
    Parameters:
        data (dict): A dictionary containing the 'now playing' information.
    """
    # Format the 'now playing' information into a readable string
    log_message_content = (
        f"Now Playing: {data['title']} by {data['artist']} from the album {data['album']} "
        f"[{data['time']}/{data['duration']} seconds]"
    )
    # Log the formatted string to the Kodi log
    log_message(log_message_content, xbmc.LOGINFO)

