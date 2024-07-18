import xbmc
import traceback
import os  # Import os module to use os.path.basename
from resources.lib.utils.constants import LOG_LEVEL_ERROR, LOG_MSG_FORMAT, LOG_ERROR_MSG_FORMAT

def log_message(message, level=xbmc.LOGINFO):
    """
    Log a message to the Kodi log with the specified log level.
    
    Parameters:
        message (str): The message to log.
        level (int): The log level for the message. Default is xbmc.LOGINFO.
    """
    try:
        # Extract the current file name and line number
        stack = traceback.extract_stack()
        filename, lineno, _, _ = stack[-2]
        filename = os.path.basename(filename)  # Get only the filename
        
        # Format the log message with file name and line number
        formatted_message = LOG_MSG_FORMAT.format(filename=filename, lineno=lineno, message=message)
        
        xbmc.log(formatted_message, level=level)
    except Exception as e:
        # Log any errors encountered during logging
        xbmc.log(LOG_ERROR_MSG_FORMAT.format(error=e), level=LOG_LEVEL_ERROR)

