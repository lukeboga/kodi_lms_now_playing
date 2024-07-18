import time
import threading
from urllib.parse import unquote
from queue import Queue, Empty
import resources.lib.utils.global_config as global_config
from resources.lib.utils.log_message import log_message
from resources.lib.utils.error_handling import log_exception
from resources.lib.deps import telnetlib
from resources.lib.api.fetch_lms_status import fetch_lms_status
from resources.lib.utils.network_utils import is_port_open, log_network_issue
from resources.lib.utils.constants import (
    BATCH_SIZE,
    EVENT_QUEUE_TIMEOUT,
    LMS_SERVER_KEY,
    LMS_TELNET_PORT_KEY,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_INFO,
    LOG_LEVEL_WARNING,
    RETRY_INTERVAL,
    TELNET_SUBSCRIBE_COMMAND,
    TELNET_UNSUBSCRIBE_COMMAND
)

class TelnetHandler:
    def __init__(self):
        self.telnet_connection = None
        self.subscriber_thread = None
        self.event_queue = Queue(maxsize=5)  # Bounded queue with max size of 5
        self.debounce_timer = None
        self.update_ui_callback = None
        self.stop_event = threading.Event()
        self.event_processor_thread = None
        self.event_available = threading.Event()  # Event to signal new data availability

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
        settings = global_config.settings
        host = settings[LMS_SERVER_KEY]
        port = int(settings[LMS_TELNET_PORT_KEY])  # Convert port to integer
        tn = None

        while tn is None and not self.stop_event.is_set():
            if not is_port_open(host, port):
                log_network_issue(f"LMS server port {port} is not open.")
                time.sleep(RETRY_INTERVAL)
                continue

            try:
                tn = telnetlib.Telnet(host, port)
                tn.write(TELNET_SUBSCRIBE_COMMAND)  # Subscribe to playlist events
                log_message("Connected to LMS via telnet.", LOG_LEVEL_INFO)
            except Exception as e:
                log_message(f"Connection failed, retrying in {RETRY_INTERVAL} seconds... Error: {e}", LOG_LEVEL_ERROR)
                log_exception(e)
                time.sleep(RETRY_INTERVAL)

        self.telnet_connection = tn
        return tn

    def handle_event(self, event_data):
        """
        Handle the received event data.
        Args:
            event_data (dict): The event data to handle.
        """
        # Ensure xbmc is imported within the thread context
        try:
            import xbmc
        except ImportError:
            pass

        # Fetch LMS data
        lms_data = fetch_lms_status()

        # Trigger the UI update callback if it's set
        if self.update_ui_callback:
            self.update_ui_callback(lms_data)

        # Clear the debounce timer
        self.debounce_timer = None

    def process_event(self):
        """
        Process the most recent event data from the queue.
        """
        batch_size = BATCH_SIZE
        while not self.stop_event.is_set():
            self.event_available.wait(timeout=1)  # Wait for the event signal or timeout
            if self.stop_event.is_set():
                break
            self.event_available.clear()  # Reset the event
            
            batch_events = []
            try:
                # Attempt to collect up to batch_size events
                for _ in range(batch_size):
                    event_data = self.event_queue.get(timeout=EVENT_QUEUE_TIMEOUT)
                    batch_events.append(event_data)
            except Empty:
                # If the queue is empty before collecting batch_size events, continue
                pass

            # Process the collected events, even if fewer than batch_size
            for event_data in batch_events:
                self.handle_event(event_data)

    def format_event_response(self, response):
        """
        Format the raw response into a dictionary with query, param, and data.
        Args:
            response (bytes): The raw response from the telnet connection.
        Returns:
            dict: The formatted event data.
        """
        parts = response.decode('utf-8').strip().split(' ')
        
        if len(parts) >= 3:
            query = parts[1]
            param = parts[2]
            data = ' '.join(parts[3:])
            data_decoded = unquote(data)
            return { 'query': query, 'param': param, 'data': data_decoded }
        return None

    def subscribe_to_events(self, tn):
        """
        Subscribe to events from the LMS server and add them to the event queue.
        Args:
            tn (telnetlib.Telnet): A telnet connection instance.
        """
        while not self.stop_event.is_set():
            try:
                response = tn.read_until(b"\n", timeout=1)  # Use timeout to periodically check stop_event
                if self.stop_event.is_set():
                    break
                event_dict = self.format_event_response(response)

                if event_dict:
                    query = event_dict['query']
                    param = event_dict['param']
                    data = event_dict['data']
                
                    if query == 'playlist' and param == 'newsong':
                        log_message(f"New response: {query}, {param}, {data}")
                        self.event_queue.put(event_dict)
                        self.event_available.set()  # Signal that new data is available
            except (EOFError, AttributeError):
                if self.stop_event.is_set():
                    break
                log_message("Connection lost, reconnecting...", LOG_LEVEL_WARNING)
                tn = self.connect_to_lms()

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
        if self.event_processor_thread is None or not self.event_processor_thread.is_alive():
            self.event_processor_thread = threading.Thread(target=self.process_event)
            self.event_processor_thread.daemon = True
            self.event_processor_thread.start()

    def close_telnet_connection(self):
        """
        Close the telnet connection and unsubscribe from events.
        Ensure all threads, events, and resources are properly terminated and cleaned up.
        """
        # Set the stop event to signal all threads to stop
        self.stop_event.set()
        
        # Signal the event_available to wake up the process_event method if it's waiting
        self.event_available.set()
        
        # Join the subscriber_thread to ensure it has completed
        if self.subscriber_thread is not None:
            self.subscriber_thread.join(timeout=5)
            if self.subscriber_thread.is_alive():
                log_message("Warning: subscriber_thread did not terminate within the timeout.", LOG_LEVEL_WARNING)
        
        # Join the event_processor_thread to ensure it has completed
        if self.event_processor_thread is not None:
            self.event_processor_thread.join(timeout=5)
            if self.event_processor_thread.is_alive():
                log_message("Warning: event_processor_thread did not terminate within the timeout.", LOG_LEVEL_WARNING)
        
        # Close the telnet connection properly
        if self.telnet_connection:
            try:
                self.telnet_connection.write(TELNET_UNSUBSCRIBE_COMMAND)  # Unsubscribe from playlist events
                self.telnet_connection.close()
                log_message("Telnet connection closed and unsubscribed from events.", LOG_LEVEL_INFO)
            except Exception as e:
                log_message(f"Error closing telnet connection: {e}", LOG_LEVEL_ERROR)
                log_exception(e)
        
        # Ensure the telnet connection is set to None
        self.telnet_connection = None

# Instantiate the TelnetHandler
telnet_handler = TelnetHandler()

