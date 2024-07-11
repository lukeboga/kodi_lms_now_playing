import re
import xbmc

def validate_ip(ip_address):
    """
    Validate an IP address format.
    
    Parameters:
        ip_address (str): The IP address to validate.
    
    Returns:
        bool: True if the IP address is valid, False otherwise.
    """
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if pattern.match(ip_address):
        return True
    else:
        xbmc.log(f"KLMS Addon: Invalid IP address format: {ip_address}", level=xbmc.LOGWARNING)
        return False

