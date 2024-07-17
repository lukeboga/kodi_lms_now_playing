import time
import threading
import xbmc
from queue import Queue, Empty
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.log_message import log_message
from resources.lib.utils.error_handling import log_exception
from resources.lib.deps import telnetlib
from resources.lib.api.fetch_lms_status import fetch_lms_status  # Ensure this is imported to fetch LMS status

# Global telnet connection instance and thread instance
telnet_connection = None
subscriber_thread = None
event_queue = Queue()
debounce_timer = None
update_ui_callback = None  # Global callback function

def set_update_ui_callback(callback):
    """
    Set the callback function for updating the UI.
    
    Args:
        callback (function): The callback function to set.
    """
    global update_ui_callback
    update_ui_callback = callback

def connect_to_lms():
    """
    Establish a telnet connection to the LMS server using settings from the configuration.
    
    Returns:
        telnetlib.Telnet: A telnet connection instance.
    """
    global telnet_connection
    settings = read_settings()
    host = settings['lms_server']
    port = settings['lms_telnet_port']
    tn = None

    while tn is None:
        try:
            tn = telnetlib.Telnet(host, port)
            tn.write(b"subscribe playlist\n")  # Subscribe to playlist events
            log_message("Connected to LMS via telnet.")
        except Exception as e:
            log_message(f"Connection failed, retrying in 5 seconds... Error: {e}", xbmc.LOGERROR)
            log_exception(e)
            time.sleep(5)

    telnet_connection = tn
    return tn

def process_event():
    """
    Process the most recent event data from the queue.
    """
    global debounce_timer

    def handle_event(event_data):
        # Ensure xbmc is imported within the thread context
        try:
            import xbmc
        except ImportError:
            pass

        # Fetch LMS data
        lms_data = fetch_lms_status()
        log_message(f"Received event: {event_data}")

        # Trigger the UI update callback if it's set
        if update_ui_callback:
            update_ui_callback(lms_data)

        # Clear the debounce timer
        debounce_timer = None

    while True:
        try:
            # Wait for an event with a timeout to allow thread to exit cleanly
            event_data = event_queue.get(timeout=1)
            if event_data:
                # Cancel any existing timer
                if debounce_timer:
                    debounce_timer.cancel()
                
                # Start a new timer
                debounce_timer = threading.Timer(1.0, handle_event, args=(event_data,))  # 1-second debounce time
                debounce_timer.start()
        except Empty:
            continue

def subscribe_to_events(tn):
    """
    Subscribe to events from the LMS server and add them to the event queue.
    
    Args:
        tn (telnetlib.Telnet): A telnet connection instance.
    """
    while True:
        try:
            response = tn.read_until(b"\n")
            event_queue.put(response.decode('utf-8'))
        except EOFError:
            log_message("Connection lost, reconnecting...", xbmc.LOGWARNING)
            connect_to_lms()

def start_telnet_subscriber():
    """
    Start threads to subscribe to LMS events via telnet and process them.
    """
    global subscriber_thread

    # Start the telnet subscription thread
    if subscriber_thread is None or not subscriber_thread.is_alive():
        tn = connect_to_lms()
        subscriber_thread = threading.Thread(target=subscribe_to_events, args=(tn,))
        subscriber_thread.daemon = True
        subscriber_thread.start()

    # Start the event processing thread
    event_processor_thread = threading.Thread(target=process_event)
    event_processor_thread.daemon = True
    event_processor_thread.start()

def close_telnet_connection():
    """
    Close the telnet connection and unsubscribe from events.
    """
    global telnet_connection
    if telnet_connection:
        try:
            telnet_connection.write(b"subscribe 0\n")  # Unsubscribe from playlist events
            telnet_connection.close()
            log_message("Telnet connection closed and unsubscribed from events.", xbmc.LOGINFO)
        except Exception as e:
            log_message(f"Error closing telnet connection: {e}", xbmc.LOGERROR)
            log_exception(e)

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`: Part of the Kodi API, used for logging.
   - `threading`: For handling multiple threads.
   - `time`: For handling time-related functions.
   - `Queue, Empty`: For handling queue operations and exceptions.
   - `read_settings`, `log_message`, `log_exception`, `fetch_lms_status`: Custom utility functions and modules.
   - `telnetlib`: Imported from `resources.lib.deps`.

2. **Global Variables:**
   - `telnet_connection`, `subscriber_thread`, `event_queue`, `debounce_timer`, `update_ui_callback`: Various global instances for managing the telnet connection and events.

3. **set_update_ui_callback Function:**
   - **Purpose:** Sets the callback function for updating the UI.
   - **Args:** `callback (function)`: The callback function to set.

4. **connect_to_lms Function:**
   - **Purpose:** Establishes a telnet connection to the LMS server using settings from the configuration.
   - **Returns:** `telnetlib.Telnet`: A telnet connection instance.
   - **Steps:** Attempts to connect to LMS, retries every 5 seconds if connection fails.

5. **process_event Function:**
   - **Purpose:** Processes the most recent event data from the queue.
   - **Steps:** Debounces the events, fetches LMS data, and triggers the UI update callback.

6. **subscribe_to_events Function:**
   - **Purpose:** Subscribes to events from the LMS server and adds them to the event queue.
   - **Args:** `tn (telnetlib.Telnet)`: A telnet connection instance.
   - **Steps:** Reads events from LMS and puts them in the event queue.

7. **start_telnet_subscriber Function:**
   - **Purpose:** Starts threads to subscribe to LMS events via telnet and process them.
   - **Steps:** Starts telnet subscription and event processing threads.

8. **close_telnet_connection Function:**
   - **Purpose:** Closes the telnet connection and unsubscribes from events.
   - **Steps:** Sends unsubscribe command to LMS and closes the connection.

"""

