import time
import threading
import xbmc
from queue import Queue, Empty
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.log_message import log_message
from resources.lib.deps import telnetlib

# Global telnet connection instance and thread instance
telnet_connection = None
subscriber_thread = None
event_queue = Queue()
debounce_timer = None

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

        log_message(f"Received event: {event_data}")

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
            tn = connect_to_lms()

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

