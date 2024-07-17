import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import socket
from contextlib import closing
from resources.lib.utils.log_message import log_message
import xbmc  # Ensure xbmc is imported for logging levels
from resources.lib.utils.constants import (
    RETRY_COUNT,
    BACKOFF_FACTOR,
    STATUS_FORCE_LIST,
    SOCKET_TIMEOUT,
    LOG_LEVEL_ERROR,
    NETWORK_ISSUE_LOG_MSG
)

def create_requests_session(retries=RETRY_COUNT, backoff_factor=BACKOFF_FACTOR, status_forcelist=STATUS_FORCE_LIST):
    """
    Create a requests session with retry logic.

    Args:
        retries (int): The number of retries.
        backoff_factor (float): A backoff factor to apply between attempts.
        status_forcelist (tuple): A set of HTTP status codes that we should force a retry on.

    Returns:
        requests.Session: A configured requests session.

    Raises:
        requests.RequestException: If the session configuration fails.
    """
    try:
        session = requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    except requests.RequestException as e:
        log_network_issue(f"Failed to create requests session: {e}")
        raise

def is_port_open(host, port, timeout=SOCKET_TIMEOUT):
    """
    Check if a port is open on a given host.

    Args:
        host (str): The host address.
        port (int): The port number.
        timeout (int): The timeout for the connection attempt in seconds.

    Returns:
        bool: True if the port is open, False otherwise.
    """
    try:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except socket.error as e:
        log_network_issue(f"Socket error while checking port {port} on host {host}: {e}")
        return False

def log_network_issue(message):
    """
    Log a network-related issue.

    Args:
        message (str): The message to log.
    """
    log_message(NETWORK_ISSUE_LOG_MSG.format(message=message), LOG_LEVEL_ERROR)

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `requests`, `HTTPAdapter`, `Retry`: Used for making HTTP requests with retry logic.
   - `socket`, `closing`: Used for checking if a port is open.
   - `log_message`: Custom function for logging messages.
   - `xbmc`: Part of the Kodi API, used for logging levels.
   - Constants imported from `constants.py`.

2. **create_requests_session Function:**
   - **Purpose:** Creates a requests session with retry logic.
   - **Args:**
     - `retries (int)`: The number of retries.
     - `backoff_factor (float)`: A backoff factor to apply between attempts.
     - `status_forcelist (tuple)`: A set of HTTP status codes that should force a retry.
   - **Returns:** A configured requests session.
   - **Raises:** `requests.RequestException` if the session configuration fails.
   - **Steps:**
     - Creates a `Retry` object with the specified parameters.
     - Creates an `HTTPAdapter` with the retry configuration.
     - Mounts the adapter to the session for both HTTP and HTTPS.
     - Logs and raises an exception if the session configuration fails.

3. **is_port_open Function:**
   - **Purpose:** Checks if a port is open on a given host.
   - **Args:**
     - `host (str)`: The host address.
     - `port (int)`: The port number.
     - `timeout (int)`: The timeout for the connection attempt in seconds.
   - **Returns:** True if the port is open, False otherwise.
   - **Steps:**
     - Creates a socket and tries to connect to the specified host and port.
     - Returns the result of the connection attempt.
     - Logs a network issue if a socket error occurs.

4. **log_network_issue Function:**
   - **Purpose:** Logs a network-related issue.
   - **Args:**
     - `message (str)

"""
