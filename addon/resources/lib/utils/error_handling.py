import xbmc
import traceback
from resources.lib.utils.constants import LOG_LEVEL_ERROR, EXCEPTION_LOG_MSG, TRACEBACK_LOG_MSG

def log_exception(exc):
    """
    Log an exception with its traceback to the Kodi log.
    
    Parameters:
        exc (Exception): The exception to log.
    """
    # Format the traceback
    exc_traceback = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    
    # Log the exception type, message, and traceback
    xbmc.log(EXCEPTION_LOG_MSG.format(exc=exc), level=LOG_LEVEL_ERROR)
    xbmc.log(TRACEBACK_LOG_MSG.format(traceback=exc_traceback), level=LOG_LEVEL_ERROR)

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`: Part of the Kodi API, used for logging.
   - `traceback`: Python module for extracting, formatting, and printing stack traces of programs.
   - Constants imported from `constants.py`.

2. **log_exception Function:**
   - **Purpose:** This function logs an exception with its traceback to the Kodi log.
   
   - **Parameters:**
     - `exc (Exception)`: The exception to log.
   
   - **Steps:**
     - Formats the traceback of the exception.
     - Logs the exception type, message, and formatted traceback.
   
   - **Detailed Steps:**
     - `exc_traceback = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))`: Formats the traceback of the exception.
     - `xbmc.log(EXCEPTION_LOG_MSG.format(exc=exc), level=LOG_LEVEL_ERROR)`: Logs the exception type and message.
     - `xbmc.log(TRACEBACK_LOG_MSG.format(traceback=exc_traceback), level=LOG_LEVEL_ERROR)`: Logs the formatted traceback.
"""

