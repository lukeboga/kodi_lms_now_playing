# `__init__` Method

## Purpose:
The `__init__` method is the constructor for the `TelnetHandler` class. It initializes the instance variables and sets up the initial state for an object of the `TelnetHandler` class. This method is called automatically when a new instance of the class is created.

## Code Breakdown:

```python
def __init__(self):
    self.telnet_connection = None
    self.subscriber_thread = None
    self.event_queue = Queue(maxsize=5)  # Bounded queue with max size of 5
    self.debounce_timer = None
    self.update_ui_callback = None
    self.stop_event = threading.Event()
    self.event_processor_thread = None
    self.event_available = threading.Event()  # Event to signal new data availability
```

## Explanation and Concepts:

1. **`self.telnet_connection = None`**:
   - This line initializes the `telnet_connection` attribute to `None`. 
   - **Concept**: An attribute is a variable that belongs to an object. Here, `telnet_connection` will later hold the Telnet connection object once a connection is established.

2. **`self.subscriber_thread = None`**:
   - Initializes the `subscriber_thread` attribute to `None`.
   - **Concept**: This attribute will hold a thread object responsible for subscribing to events from the LMS (Logitech Media Server).

3. **`self.event_queue = Queue(maxsize=5)`**:
   - Creates a queue with a maximum size of 5 and assigns it to the `event_queue` attribute.
   - **Concept**: A queue is a data structure that follows the First In, First Out (FIFO) principle. Here, it is used to hold events to be processed. The `maxsize` argument limits the number of items that can be stored in the queue at any one time to 5. Using a bounded queue helps prevent memory overflow.

4. **`self.debounce_timer = None`**:
   - Initializes the `debounce_timer` attribute to `None`.
   - **Concept**: A debounce timer is used to limit the rate at which a function is executed. Here, it will be used to manage delays in handling events to prevent excessive function calls.

5. **`self.update_ui_callback = None`**:
   - Initializes the `update_ui_callback` attribute to `None`.
   - **Concept**: This attribute will hold a callback function that updates the user interface (UI). A callback function is a function that is passed as an argument to another function and is invoked after some kind of event.

6. **`self.stop_event = threading.Event()`**:
   - Creates an event object and assigns it to the `stop_event` attribute.
   - **Concept**: An event is a synchronization primitive that can be used to signal between threads. The `stop_event` will be used to signal threads to stop running, facilitating a graceful shutdown of the threads.

7. **`self.event_processor_thread = None`**:
   - Initializes the `event_processor_thread` attribute to `None`.
   - **Concept**: This attribute will hold a thread object responsible for processing events from the queue.

8. **`self.event_available = threading.Event()`**:
   - Creates an event object and assigns it to the `event_available` attribute.
   - **Concept**: This event is used to signal the availability of new data. When an event is added to the queue, this event will be set to notify the `event_processor_thread`.

## How This Method Relates to Other Methods:

- **Setup for `connect_to_lms`**: The `telnet_connection` attribute is initialized to `None`, and will be set up by the `connect_to_lms` method.
  
- **Threads Setup for `start_telnet_subscriber`**: The `subscriber_thread` and `event_processor_thread` attributes are initialized to `None`, and these will be created and started in the `start_telnet_subscriber` method.

- **Event Handling**: The `event_queue`, `stop_event`, and `event_available` attributes are used in methods like `process_event` and `subscribe_to_events` for managing events and inter-thread communication.

- **UI Updates**: The `update_ui_callback` attribute is set up to store a callback function, which will be called in the `handle_event` method to update the UI.

# `set_update_ui_callback` Method

## Purpose:
The `set_update_ui_callback` method is used to set a callback function that will be called to update the user interface (UI) whenever new event data is processed.

## Code Breakdown:

```python
def set_update_ui_callback(self, callback):
    """
    Set the callback function for updating the UI.
    Args:
        callback (function): The callback function to set.
    """
    self.update_ui_callback = callback
```

## Explanation and Concepts:

1. **Method Definition**:
   - The method is defined with `self` and `callback` as parameters.
   - **Concept**: `self` refers to the instance of the class, allowing access to its attributes and methods. `callback` is the function that will be passed to this method when it is called.

2. **Docstring**:
   - The docstring explains the purpose of the method and its arguments.
   - **Concept**: Docstrings provide documentation for the method, explaining what it does and what parameters it accepts. This is useful for understanding the code later on or for others who might use the code.

3. **Setting the Callback**:
   - The line `self.update_ui_callback = callback` assigns the passed `callback` function to the `update_ui_callback` attribute of the instance.
   - **Concept**: This allows the class to store the callback function and call it later when needed. By using a callback, the class can notify other parts of the application about new events or data.

## How This Method Relates to Other Methods:

- **Initialization**: This method is typically called during the initialization or setup phase of the application, after creating an instance of `TelnetHandler`. For example, it might be called in the `__init__` method of another class that uses `TelnetHandler`.

- **Event Handling**: The `update_ui_callback` attribute is used in the `handle_event` method. When new event data is processed, the callback function stored in `update_ui_callback` is called to update the UI.

- **Example Usage**:
   ```python
   telnet_handler = TelnetHandler()

   def update_ui(data):
       # Code to update the UI with the new data
       pass

   telnet_handler.set_update_ui_callback(update_ui)

# `connect_to_lms` Method

## Purpose:
The `connect_to_lms` method establishes a Telnet connection to the LMS (Logitech Media Server). This connection is necessary for subscribing to events and receiving data from the server.

## Code Breakdown:

```python
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
```

## Explanation and Concepts:

1. **Retrieve Configuration Settings**:
   ```python
   settings = global_config.settings
   host = settings[LMS_SERVER_KEY]
   port = int(settings[LMS_TELNET_PORT_KEY])
   ```
   - **Concept**: `global_config.settings` contains configuration settings for the application, including the LMS server details. This method retrieves the server's host and port from these settings.
   - **Reasoning**: These details are necessary to establish a connection to the LMS server.

2. **Initialize Connection Variable**:
   ```python
   tn = None
   ```
   - **Concept**: `tn` is initialized to `None` to indicate that there is no active Telnet connection yet.
   - **Reasoning**: This variable will later hold the Telnet connection instance.

3. **Loop Until Connection is Established or Stop Event is Set**:
   ```python
   while tn is None and not self.stop_event.is_set():
   ```
   - **Concept**: This loop continues to run until a connection is successfully established (`tn` is not `None`) or the stop event (`self.stop_event`) is set.
   - **Reasoning**: This ensures that the method keeps trying to connect until it succeeds or is explicitly stopped.

4. **Check if Port is Open**:
   ```python
   if not is_port_open(host, port):
       log_network_issue(f"LMS server port {port} is not open.")
       time.sleep(RETRY_INTERVAL)
       continue
   ```
   - **Concept**: `is_port_open(host, port)` checks if the specified port on the host is open.
   - **Reasoning**: If the port is not open, the method logs a network issue, waits for a retry interval, and then continues to the next iteration of the loop. This avoids trying to connect to a closed port.

5. **Attempt to Establish Telnet Connection**:
   ```python
   try:
       tn = telnetlib.Telnet(host, port)
       tn.write(TELNET_SUBSCRIBE_COMMAND)  # Subscribe to playlist events
       log_message("Connected to LMS via telnet.", LOG_LEVEL_INFO)
   except Exception as e:
       log_message(f"Connection failed, retrying in {RETRY_INTERVAL} seconds... Error: {e}", LOG_LEVEL_ERROR)
       log_exception(e)
       time.sleep(RETRY_INTERVAL)
   ```
   - **Concept**: The method attempts to create a Telnet connection to the LMS server using `telnetlib.Telnet(host, port)`. If successful, it sends a command to subscribe to playlist events and logs a success message.
   - **Reasoning**: This is the core operation of the method. If an exception occurs (e.g., connection failure), it logs the error, waits for the retry interval, and tries again.

6. **Store and Return the Connection**:
   ```python
   self.telnet_connection = tn
   return tn
   ```
   - **Concept**: Once a connection is successfully established, it is stored in the `self.telnet_connection` attribute and returned.
   - **Reasoning**: This allows other methods in the class to use the established connection.

## How This Method Relates to Other Methods:

- **`subscribe_to_events`**: This method calls `connect_to_lms` to get the Telnet connection before subscribing to events.
- **`start_telnet_subscriber`**: This method starts the thread that runs `subscribe_to_events`, which in turn uses `connect_to_lms` to establish the connection.
- **Error Handling**: If the connection fails, the method logs the error and retries, ensuring robustness and reliability in establishing the connection.


# `subscribe_to_events` Method

## Purpose:
The `subscribe_to_events` method subscribes to events from the LMS (Logitech Media Server) using the established Telnet connection and adds these events to the event queue for further processing.

## Code Breakdown:

```python
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
```

## Explanation and Concepts:

1. **Method Signature and Docstring**:
   ```python
   def subscribe_to_events(self, tn):
       """
       Subscribe to events from the LMS server and add them to the event queue.
       Args:
           tn (telnetlib.Telnet): A telnet connection instance.
       """
   ```
   - **Concept**: The method takes a `telnetlib.Telnet` instance (`tn`) as an argument and subscribes to events from the LMS server.
   - **Reasoning**: This method uses the established Telnet connection to receive data and process it.

2. **Continuous Loop with Stop Event Check**:
   ```python
   while not self.stop_event.is_set():
   ```
   - **Concept**: The method runs in a continuous loop until the `stop_event` is set.
   - **Reasoning**: This ensures the method keeps running to continuously receive events unless it is explicitly stopped.

3. **Read Response from Telnet Connection**:
   ```python
   try:
       response = tn.read_until(b"\n", timeout=1)  # Use timeout to periodically check stop_event
       if self.stop_event.is_set():
           break
       event_dict = self.format_event_response(response)
   ```
   - **Concept**: The method attempts to read a response from the Telnet connection until a newline character (`\n`) is encountered, with a timeout of 1 second.
   - **Reasoning**: The timeout allows the method to periodically check if the `stop_event` is set, ensuring it can gracefully exit if needed.

4. **Check for Stop Event Again**:
   ```python
   if self.stop_event.is_set():
       break
   ```
   - **Concept**: Immediately after reading the response, the method checks if the `stop_event` is set.
   - **Reasoning**: This ensures that the method can exit promptly if the stop event is triggered during the read operation.

5. **Format the Event Response**:
   ```python
   event_dict = self.format_event_response(response)
   ```
   - **Concept**: The method calls `self.format_event_response(response)` to convert the raw response into a dictionary.
   - **Reasoning**: This formatting makes it easier to work with the event data.

6. **Process the Event Data**:
   ```python
   if event_dict:
       query = event_dict['query']
       param = event_dict['param']
       data = event_dict['data']
   
       if query == 'playlist' and param == 'newsong':
           log_message(f"New response: {query}, {param}, {data}")
           self.event_queue.put(event_dict)
           self.event_available.set()  # Signal that new data is available
   ```
   - **Concept**: If the `event_dict` is not `None`, it extracts the `query`, `param`, and `data` from the dictionary.
   - **Reasoning**: These values are necessary to determine the type of event and its relevant data.
   - **Filter and Log**: The method checks if the `query` is `playlist` and `param` is `newsong`. If so, it logs the event and adds it to the event queue. It also signals that new data is available.
     - **Reasoning**: Filtering ensures that only relevant events are processed, and signaling the availability of new data triggers the event processing mechanism.

7. **Exception Handling**:
   ```python
   except (EOFError, AttributeError):
       if self.stop_event.is_set():
           break
       log_message("Connection lost, reconnecting...", LOG_LEVEL_WARNING)
       tn = self.connect_to_lms()
   ```
   - **Concept**: The method handles `EOFError` and `AttributeError` exceptions, which may occur during the read operation.
   - **Reasoning**: If an exception occurs and the `stop_event` is not set, the method logs a warning and attempts to reconnect to the LMS server. This ensures robustness and resilience in maintaining the connection.

## How This Method Relates to Other Methods:

- **`connect_to_lms`**: This method is called within `subscribe_to_events` to establish or re-establish the Telnet connection as needed.
- **`format_event_response`**: This method is used to format the raw response into a structured dictionary.
- **`process_event`**: Events added to the `event_queue` are processed by the `process_event` method, which handles the logic for dealing with these events.
- **`close_telnet_connection`**: This method sets the `stop_event`, signaling `subscribe_to_events` to stop its loop and exit gracefully.


# `process_event` Method

## Purpose:
The `process_event` method processes the most recent event data from the event queue. It attempts to collect events in batches and handles them appropriately.

## Code Breakdown:

```python
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
```

## Explanation and Concepts:

1. **Method Signature and Docstring**:
   ```python
   def process_event(self):
       """
       Process the most recent event data from the queue.
       """
   ```
   - **Concept**: This method processes events that have been added to the event queue.
   - **Reasoning**: This method is necessary to handle and act upon the events received from the LMS server.

2. **Batch Size Configuration**:
   ```python
   batch_size = BATCH_SIZE
   ```
   - **Concept**: The `batch_size` is set to a predefined constant value.
   - **Reasoning**: Processing events in batches can improve efficiency by reducing the overhead of handling each event individually.

3. **Continuous Loop with Stop Event Check**:
   ```python
   while not self.stop_event.is_set():
   ```
   - **Concept**: The method runs in a continuous loop until the `stop_event` is set.
   - **Reasoning**: This ensures the method keeps running to continuously process events unless it is explicitly stopped.

4. **Wait for Event Signal or Timeout**:
   ```python
   self.event_available.wait(timeout=1)  # Wait for the event signal or timeout
   if self.stop_event.is_set():
       break
   self.event_available.clear()  # Reset the event
   ```
   - **Concept**: The method waits for the `event_available` signal or a timeout of 1 second.
   - **Reasoning**: The `wait` method ensures that the loop does not run continuously, wasting CPU resources. It only proceeds when an event is available or after a timeout. If the `stop_event` is set, the loop breaks, allowing for graceful shutdown.

5. **Initialize Batch Events List**:
   ```python
   batch_events = []
   ```
   - **Concept**: An empty list is initialized to store the batch of events.
   - **Reasoning**: This list will hold the events collected from the queue for batch processing.

6. **Collect Events from Queue**:
   ```python
   try:
       # Attempt to collect up to batch_size events
       for _ in range(batch_size):
           event_data = self.event_queue.get(timeout=EVENT_QUEUE_TIMEOUT)
           batch_events.append(event_data)
   except Empty:
       # If the queue is empty before collecting batch_size events, continue
       pass
   ```
   - **Concept**: The method attempts to collect up to `batch_size` events from the queue, with a timeout for each `get` operation.
   - **Reasoning**: Using a timeout for `get` ensures that the method does not block indefinitely if the queue is empty. The `Empty` exception is caught to handle cases where fewer than `batch_size` events are available.

7. **Process Collected Events**:
   ```python
   # Process the collected events, even if fewer than batch_size
   for event_data in batch_events:
       self.handle_event(event_data)
   ```
   - **Concept**: The method processes each event in the `batch_events` list using the `handle_event` method.
   - **Reasoning**: Processing events in batches improves efficiency and ensures that all collected events are handled, even if fewer than `batch_size` events are available.

## How This Method Relates to Other Methods:

- **`subscribe_to_events`**: This method adds events to the `event_queue`, which `process_event` then processes.
- **`handle_event`**: This method is called for each event in the batch to handle the event's specific logic.
- **`close_telnet_connection`**: This method sets the `stop_event`, signaling `process_event` to stop its loop and exit gracefully.

# `handle_event` Method

## Purpose:
The `handle_event` method processes individual event data. It fetches the latest LMS (Logitech Media Server) data and updates the UI if a callback is set.

## Code Breakdown:

```python
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
```

## Explanation and Concepts:

1. **Method Signature and Docstring**:
   ```python
   def handle_event(self, event_data):
       """
       Handle the received event data.
       Args:
           event_data (dict): The event data to handle.
       """
   ```
   - **Concept**: This method processes the event data received.
   - **Reasoning**: Handling event data is crucial for updating the application state based on the received events.

2. **Ensure `xbmc` is Imported**:
   ```python
   try:
       import xbmc
   except ImportError:
       pass
   ```
   - **Concept**: Import `xbmc` within the thread context.
   - **Reasoning**: Ensuring `xbmc` is available within the thread context is necessary for performing UI updates in Kodi. The `try` block handles cases where the import might fail.

3. **Fetch LMS Data**:
   ```python
   lms_data = fetch_lms_status()
   ```
   - **Concept**: Retrieve the latest data from the LMS.
   - **Reasoning**: Fetching the latest data ensures that the application reacts to the most current state of the media server.

4. **Trigger the UI Update Callback**:
   ```python
   if self.update_ui_callback:
       self.update_ui_callback(lms_data)
   ```
   - **Concept**: Call the `update_ui_callback` if it is set.
   - **Reasoning**: The callback updates the UI with the latest LMS data, ensuring the user interface reflects the current state.

5. **Clear the Debounce Timer**:
   ```python
   self.debounce_timer = None
   ```
   - **Concept**: Reset the debounce timer.
   - **Reasoning**: Clearing the debounce timer ensures that subsequent events are not delayed unnecessarily.

## How This Method Relates to Other Methods:

- **`process_event`**: This method calls `handle_event` for each event data processed. Understanding `handle_event` is crucial for comprehending how events are handled within the `process_event` method.
- **`set_update_ui_callback`**: This method sets the `update_ui_callback` used in `handle_event`. The callback mechanism is crucial for updating the UI based on the latest LMS data.
- **`fetch_lms_status`**: This method retrieves the LMS data needed by `handle_event` to update the UI.

# `format_event_response` Method

## Purpose:
The `format_event_response` method is responsible for formatting the raw response from the telnet connection into a structured dictionary with keys `query`, `param`, and `data`. This makes it easier to handle and process the data in subsequent methods.

## Code Breakdown:

```python
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
```

## Explanation and Concepts:

1. **Method Signature and Docstring**:
   ```python
   def format_event_response(self, response):
       """
       Format the raw response into a dictionary with query, param, and data.
       Args:
           response (bytes): The raw response from the telnet connection.
       Returns:
           dict: The formatted event data.
       """
   ```
   - **Concept**: Define the method with a single parameter, `response`, which is a byte string containing the raw response from the telnet connection.
   - **Reasoning**: The method aims to convert this byte string into a more usable dictionary format.

2. **Decode the Response and Split into Parts**:
   ```python
   parts = response.decode('utf-8').strip().split(' ')
   ```
   - **Concept**: Decode the byte string into a UTF-8 string, strip any leading or trailing whitespace, and split it into parts using spaces as the delimiter.
   - **Reasoning**: Decoding the byte string makes it readable, and splitting it into parts helps extract specific elements (query, param, and data).

3. **Check the Length of Parts**:
   ```python
   if len(parts) >= 3:
   ```
   - **Concept**: Check if the `parts` list contains at least three elements.
   - **Reasoning**: Ensure that there are enough parts to form a valid query, param, and data. If not, return `None`.

4. **Extract Query and Param**:
   ```python
   query = parts[1]
   param = parts[2]
   ```
   - **Concept**: Extract the second and third elements from the `parts` list as `query` and `param`.
   - **Reasoning**: The first element (usually an identifier) is ignored, and the second and third elements are typically the query and param.

5. **Extract and Decode Data**:
   ```python
   data = ' '.join(parts[3:])
   data_decoded = unquote(data)
   ```
   - **Concept**: Join the remaining elements in the `parts` list to form the `data` string. Decode any URL-encoded characters using `unquote`.
   - **Reasoning**: The remaining elements form the data, which may contain URL-encoded characters that need to be decoded for readability.

6. **Return the Formatted Event Data**:
   ```python
   return { 'query': query, 'param': param, 'data': data_decoded }
   ```
   - **Concept**: Return a dictionary with `query`, `param`, and `data` keys.
   - **Reasoning**: Structuring the data in this format makes it easier to handle and process in subsequent methods.

7. **Return None if Parts are Insufficient**:
   ```python
   return None
   ```
   - **Concept**: Return `None` if the `parts` list does not contain at least three elements.
   - **Reasoning**: Avoid processing incomplete data.

## How This Method Relates to Other Methods:

- **`subscribe_to_events`**: Calls `format_event_response` to convert the raw response into a structured format before adding it to the event queue.
- **`process_event` and `handle_event`**: Use the formatted event data. Understanding the structure of the data helps in processing and handling it correctly.
- **`connect_to_lms`**: Establishes the telnet connection that receives the raw response processed by `format_event_response`.

# `close_telnet_connection` Method

## Purpose:
The `close_telnet_connection` method ensures that the telnet connection and all related threads, events, and resources are properly terminated and cleaned up. It ensures a graceful shutdown of the `TelnetHandler` class.

## Code Breakdown:

```python
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
```

## Explanation and Concepts:

1. **Method Signature and Docstring**:
   ```python
   def close_telnet_connection(self):
       """
       Close the telnet connection and unsubscribe from events.
       Ensure all threads, events, and resources are properly terminated and cleaned up.
       """
   ```
   - **Concept**: Define the method without parameters.
   - **Reasoning**: This method is designed to clean up resources related to the `TelnetHandler` instance.

2. **Set the `stop_event`**:
   ```python
   self.stop_event.set()
   ```
   - **Concept**: Set the `stop_event` to signal all threads to stop.
   - **Reasoning**: This event is used to gracefully terminate the `process_event` and `subscribe_to_events` methods.

3. **Signal the `event_available`**:
   ```python
   self.event_available.set()
   ```
   - **Concept**: Signal the `event_available` to wake up the `process_event` method if it is waiting.
   - **Reasoning**: Ensure that the `process_event` method can exit the loop promptly by setting this event.

4. **Join the `subscriber_thread`**:
   ```python
   if self.subscriber_thread is not None:
       self.subscriber_thread.join(timeout=5)
       if self.subscriber_thread.is_alive():
           log_message("Warning: subscriber_thread did not terminate within the timeout.", LOG_LEVEL_WARNING)
   ```
   - **Concept**: If the `subscriber_thread` is running, join it with a timeout of 5 seconds to ensure it has completed.
   - **Reasoning**: Wait for the thread to finish execution to ensure no resources are being used by it. Log a warning if it does not terminate within the timeout.

5. **Join the `event_processor_thread`**:
   ```python
   if self.event_processor_thread is not None:
       self.event_processor_thread.join(timeout=5)
       if self.event_processor_thread.is_alive():
           log_message("Warning: event_processor_thread did not terminate within the timeout.", LOG_LEVEL_WARNING)
   ```
   - **Concept**: If the `event_processor_thread` is running, join it with a timeout of 5 seconds to ensure it has completed.
   - **Reasoning**: Similar to the `subscriber_thread`, ensure that this thread has completed execution. Log a warning if it does not terminate within the timeout.

6. **Close the Telnet Connection**:
   ```python
   if self.telnet_connection:
       try:
           self.telnet_connection.write(TELNET_UNSUBSCRIBE_COMMAND)  # Unsubscribe from playlist events
           self.telnet_connection.close()
           log_message("Telnet connection closed and unsubscribed from events.", LOG_LEVEL_INFO)
       except Exception as e:
           log_message(f"Error closing telnet connection: {e}", LOG_LEVEL_ERROR)
           log_exception(e)
   ```
   - **Concept**: If there is an active telnet connection, unsubscribe from playlist events and close the connection. Log the status or any errors that occur.
   - **Reasoning**: Ensure that the connection is properly terminated to free up resources and avoid potential issues with open connections.

7. **Set the `telnet_connection` to `None`**:
   ```python
   self.telnet_connection = None
   ```
   - **Concept**: Set the `telnet_connection` attribute to `None`.
   - **Reasoning**: This helps ensure that the object state reflects that there is no active connection.

## How This Method Relates to Other Methods:

- **`__init__`**: Initializes the events and threads that need to be cleaned up by `close_telnet_connection`.
- **`start_telnet_subscriber`**: Starts the `subscriber_thread` and `event_processor_thread` that need to be joined and terminated in `close_telnet_connection`.
- **`subscribe_to_events` and `process_event`**: Use the `stop_event` to know when to stop execution, which is set in `close_telnet_connection`.

