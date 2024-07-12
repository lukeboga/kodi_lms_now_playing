# Import necessary modules
import re
import xbmc
from .log_message import log_message

def is_valid_ip(ip_address):
    """
    Validate the given IP address.
    
    This function checks if the provided IP address is in a valid format using a regular expression.
    
    Parameters:
        ip_address (str): The IP address to validate.
    
    Returns:
        bool: True if the IP address is valid, False otherwise.
    """
    # Regular expression for validating an IP address
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    
    # Check if the IP address matches the pattern
    if ip_pattern.match(ip_address):
        return True
    else:
        # Log a warning if the IP address is invalid
        log_message(f"Invalid IP address format: {ip_address}", xbmc.LOGWARNING)
        return False

