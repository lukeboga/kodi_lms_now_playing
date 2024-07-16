import time
import threading
import logging
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.log_message import log_message
from resources.lib.deps import telnetlib

# Global telnet connection instance
telnet_connection = None

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
            tn.write(b"listen 1\n")  # Subscribe to all events
            log_message("Connected to LMS via telnet.", logging.INFO)
        except Exception as e:
            log_message(f"Connection failed, retrying in 5 seconds... Error: {e}", logging.ERROR)
            time.sleep(5)

    telnet_connection = tn
    return tn

def process_event(event_data):
    """
    Process the event data received from the LMS server and log it.
    
    Args:
        event_data (str): The event data as a string.
    """
    lines = event_data.strip().split("\n")
    event = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            event[key.strip()] = value.strip()
        else:
            event['event'] = line.strip()
    log_message(f"Received event: {event}", logging.INFO)

def listen_for_events(tn):
    """
    Listen for events from the LMS server and process them.
    
    Args:
        tn (telnetlib.Telnet): A telnet connection instance.
    """
    while True:
        try:
            response = tn.read_until(b"\n")
            process_event(response.decode('utf-8'))
        except EOFError:
            log_message("Connection lost, reconnecting...", logging.WARNING)
            tn = connect_to_lms()

def start_telnet_listener():
    """
    Start a thread to listen for LMS events via telnet.
    """
    tn = connect_to_lms()
    listener_thread = threading.Thread(target=listen_for_events, args=(tn,))
    listener_thread.daemon = True
    listener_thread.start()

def close_telnet_connection():
    """
    Close the telnet connection and unsubscribe from events.
    """
    global telnet_connection
    if telnet_connection:
        try:
            telnet_connection.write(b"listen 0\n")  # Unsubscribe from all events
            telnet_connection.close()
            log_message("Telnet connection closed and unsubscribed from events.", logging.INFO)
        except Exception as e:
            log_message(f"Error closing telnet connection: {e}", logging.ERROR)

