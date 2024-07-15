import xbmc

def log_message(message, level=xbmc.LOGINFO):
    """
    Log a message to the Kodi log with the specified log level.
    
    Parameters:
        message (str): The message to log.
        level (int): The log level for the message. Default is xbmc.LOGINFO.
    """
    try:
        xbmc.log(f"[KLMS Addon] {message}", level=level)
    except Exception as e:
        # Log any errors encountered during logging
        xbmc.log(f"[KLMS Addon] [Error] {e}", level=xbmc.LOGERROR)

