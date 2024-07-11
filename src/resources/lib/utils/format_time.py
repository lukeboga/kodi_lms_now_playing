import xbmc

def format_time(seconds):
    """
    Convert a time value in seconds to a formatted string (MM:SS).
    
    Parameters:
        seconds (int): The time value in seconds to be converted.
    
    Returns:
        str: The formatted time string in MM:SS format.
    """
    try:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        formatted_time = f"{minutes}:{remaining_seconds:02}"
        return formatted_time
    except Exception as e:
        # Log any errors encountered during the time formatting
        xbmc.log(f"KLMS Addon: Error formatting time: {e}", level=xbmc.LOGERROR)
        return "00:00"

