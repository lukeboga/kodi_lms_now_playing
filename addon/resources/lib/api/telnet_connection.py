import xbmc
import asyncio
from resources.lib.deps.telnetlib3 import open_connection
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.log_message import log_message

async def connect_to_lms():
    """
    Establish a telnet connection to the LMS server and subscribe to events.
    """
    settings = read_settings()
    host = settings['lms_server']
    port = settings['lms_telnet_port']

    try:
        reader, writer = await open_connection(host, port)  # Update this line
        writer.write('listen 1\n')
        log_message("Connected to LMS telnet server.", xbmc.LOGINFO)
        await listen_for_events(reader)
    except Exception as e:
        log_message(f"Failed to connect to LMS telnet server: {e}", xbmc.LOGERROR)

async def listen_for_events(reader):
    """
    Listen for events from the LMS server and log the responses.
    """
    try:
        while True:
            response = await reader.read(1024)
            if response:
                log_message(f"Received event: {response.strip()}", xbmc.LOGINFO)
    except Exception as e:
        log_message(f"Error while listening for events: {e}", xbmc.LOGERROR)

def start_telnet_listener():
    """
    Start the asyncio event loop to listen for LMS events.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_to_lms())

# Ensure the connection is closed when the addon is shut down
import atexit
def close_connection():
    try:
        settings = read_settings()
        host = settings['lms_server']
        port = settings['lms_telnet_port']
        reader, writer = asyncio.run(open_connection(host, port))  # Update this line
        writer.write('listen 0\n')  # Unsubscribe from all events
        writer.close()
        log_message("Disconnected from LMS telnet server.", xbmc.LOGINFO)
    except Exception as e:
        log_message(f"Failed to disconnect from LMS telnet server: {e}", xbmc.LOGERROR)

atexit.register(close_connection)

