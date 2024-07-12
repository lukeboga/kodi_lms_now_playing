# Import necessary modules
import xbmc
from .log_message import log_message

def format_time(seconds):
    """
    Format a time duration in seconds into a string of the form H:MM:SS.
    
    This function converts a time duration given in seconds into a human-readable string format.
    
    Parameters:
        seconds (int): The time duration in seconds.
    
    Returns:
        str: The formatted time string.
    """
    try:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        formatted_time = f"{hours}:{minutes:02}:{seconds:02}"
        return formatted_time
    except Exception as e:
        # Log any errors encountered during time formatting
        log_message(f"Error formatting time: {e}", xbmc.LOGERROR)
        return "0:00:00"

