import xbmc
import traceback

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
        
        # Format the log message with file name and line number
        formatted_message = f"[KLMS Addon] {filename}:{lineno} - {message}"
        
        xbmc.log(formatted_message, level=level)
    except Exception as e:
        # Log any errors encountered during logging
        xbmc.log(f"[KLMS Addon] [Error] {e}", level=xbmc.LOGERROR)

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc` is part of the Kodi API. It provides functionalities to log messages to Kodi's log file.
   - `traceback` is a standard Python module that helps in extracting information about the stack trace.

2. **log_message Function:**
   - **Purpose:** This function logs a message to Kodi's log with the specified log level and includes information about the file name and line number where the log message originated.
   
   - **Parameters:**
     - `message`: The message to log.
     - `level`: The log level for the message. Default is `xbmc.LOGINFO`.
   
   - **Steps:**
     - The function tries to log the message along with the file name and line number.
     - If an error occurs during logging, it logs the error message.
   
   - **Detailed Steps:**
     - `stack = traceback.extract_stack()`: Extracts the current stack trace.
     - `filename, lineno, _, _ = stack[-2]`: Retrieves the file name and line number from the stack trace.
     - `formatted_message = f"[KLMS Addon] {filename}:{lineno} - {message}"`: Formats the log message to include the file name and line number.
     - `xbmc.log(formatted_message, level=level)`: Logs the formatted message to Kodi's log.
     - `except Exception as e`: If any error occurs during this process, it is caught and handled here.
     - `xbmc.log(f"[KLMS Addon] [Error] {e}", level=xbmc.LOGERROR)`: Logs the error message.
"""

