import xbmc
import traceback

def log_exception(exc):
    """
    Log an exception with its traceback to the Kodi log.
    
    Parameters:
        exc (Exception): The exception to log.
    """
    # Format the traceback
    exc_traceback = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    
    # Log the exception type, message, and traceback
    xbmc.log(f"[KLMS Addon] Exception: {exc}", level=xbmc.LOGERROR)
    xbmc.log(f"[KLMS Addon] Traceback: {exc_traceback}", level=xbmc.LOGERROR)

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`: Part of the Kodi API, used for logging.
   - `traceback`: Python module for extracting, formatting, and printing stack traces of programs.

2. **log_exception Function:**
   - **Purpose:** This function logs an exception with its traceback to the Kodi log.
   
   - **Parameters:**
     - `exc (Exception)`: The exception to log.
   
   - **Steps:**
     - Formats the traceback of the exception.
     - Logs the exception type, message, and formatted traceback.
   
   - **Detailed Steps:**
     - `exc_traceback = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))`: Formats the traceback of the exception.
     - `xbmc.log(f"[KLMS Addon] Exception: {exc}", level=xbmc.LOGERROR)`: Logs the exception type and message.
     - `xbmc.log(f"[KLMS Addon] Traceback: {exc_traceback}", level=xbmc.LOGERROR)`: Logs the formatted traceback.
"""

