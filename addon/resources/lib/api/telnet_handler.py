import time
import threading
import xbmc
from queue import Queue, Empty
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.log_message import log_message
from resources.lib.utils.error_handling import log_exception
from resources.lib.deps import telnetlib
from resources.lib.api.fetch_lms_status import fetch_lms_status
from resources.lib.utils.network_utils import is_port_open, log_network_issue

class TelnetHandler:
    def __init__(self):
        self.telnet_connection = None
        self.subscriber_thread = None
        self.event_queue = Queue()
        self.debounce_timer = None
        self.update_ui_callback = None

    def set_update_ui_callback(self, callback):
        """
        Set the callback function for updating the UI.

        Args:
            callback (function): The callback function to set.
        """
        self.update_ui_callback = callback

    def connect_to_lms(self):
        """
        Establish a telnet connection to the LMS server using settings from the configuration.

        Returns:
            telnetlib.Telnet: A telnet connection instance.
        """
        settings = read_settings()
        host = settings['lms_server']
        port = int(settings['lms_telnet_port'])  # Convert port to integer
        tn = None

        while tn is None:
            if not is_port_open(host, port):
                log_network_issue(f"LMS server port {port} is not open.")
                time.sleep(5)
                continue

            try:
                tn = telnetlib.Telnet(host, port)
                tn.write(b"subscribe playlist\n")  # Subscribe to playlist events
                log_message("Connected to LMS via telnet.")
            except Exception as e:
                log_message(f"Connection failed, retrying in 5 seconds... Error: {e}", xbmc.LOGERROR)
                log_exception(e)
                time.sleep(5)

        self.telnet_connection = tn
        return tn

    def process_event(self):
        """
        Process the most recent event data from the queue.
        """
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
            if self.update_ui_callback:
                self.update_ui_callback(lms_data)

            # Clear the debounce timer
            self.debounce_timer = None

        while True:
            try:
                # Wait for an event with a timeout to allow thread to exit cleanly
                event_data = self.event_queue.get(timeout=1)
                if event_data:
                    # Cancel any existing timer
                    if self.debounce_timer:
                        self.debounce_timer.cancel()

                    # Start a new timer
                    self.debounce_timer = threading.Timer(1.0, handle_event, args=(event_data,))  # 1-second debounce time
                    self.debounce_timer.start()
            except Empty:
                continue

    def subscribe_to_events(self, tn):
        """
        Subscribe to events from the LMS server and add them to the event queue.

        Args:
            tn (telnetlib.Telnet): A telnet connection instance.
        """
        while True:
            try:
                response = tn.read_until(b"\n")
                self.event_queue.put(response.decode('utf-8'))
            except EOFError:
                log_message("Connection lost, reconnecting...", xbmc.LOGWARNING)
                self.connect_to_lms()

    def start_telnet_subscriber(self):
        """
        Start threads to subscribe to LMS events via telnet and process them.
        """
        # Start the telnet subscription thread
        if self.subscriber_thread is None or not self.subscriber_thread.is_alive():
            tn = self.connect_to_lms()
            self.subscriber_thread = threading.Thread(target=self.subscribe_to_events, args=(tn,))
            self.subscriber_thread.daemon = True
            self.subscriber_thread.start()

        # Start the event processing thread
        event_processor_thread = threading.Thread(target=self.process_event)
        event_processor_thread.daemon = True
        event_processor_thread.start()

    def close_telnet_connection(self):
        """
        Close the telnet connection and unsubscribe from events.
        """
        if self.telnet_connection:
            try:
                self.telnet_connection.write(b"subscribe 0\n")  # Unsubscribe from playlist events
                self.telnet_connection.close()
                log_message("Telnet connection closed and unsubscribed from events.", xbmc.LOGINFO)
            except Exception as e:
                log_message(f"Error closing telnet connection: {e}", xbmc.LOGERROR)
                log_exception(e)

# Instantiate the TelnetHandler
telnet_handler = TelnetHandler()

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
   - `is_port_open`, `log_network_issue`: Custom network utility functions for checking if a port is open and logging network issues.

2. **TelnetHandler Class:**
   - **Purpose:** Manages the telnet connection, event subscription, and event processing for the KLMS Addon.
   - **Methods:**
     - `__init__`: Initializes the class variables.
     - `set_update_ui_callback`: Sets the callback function for updating the UI.
     - `connect_to_lms`: Establishes a telnet connection to the LMS server using settings from the configuration.
     - `process_event`: Processes the most recent event data from the queue, debounces events, fetches LMS data, and triggers the UI update callback.
     - `subscribe_to_events`: Subscribes to events from the LMS server and adds them to the event queue.
     - `start_telnet_subscriber`: Starts threads to subscribe to LMS events via telnet and process them.
     - `close_telnet_connection`: Closes the telnet connection and unsubscribes from events.

3. **Global Instance:**
   - `telnet_handler`: An instance of the `TelnetHandler` class, used to manage the telnet connection and events.

"""
