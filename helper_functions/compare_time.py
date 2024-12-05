import datetime

def evaluate_event_timing(event, maxAge):
    """
    Compare an event's timestamp with the current time.

    Args:
        event (dict): The event to evaluate, containing a 'timestamp' key.
        maxAge (int or float): The maximum allowed age in seconds for the event.

    Returns:
        str: "too old" if the event is older than maxAge seconds, otherwise "fire".
        bool: True if the event is valid (you should fire it), False if it's too old.
    """
    # Parse the event's timestamp
    maxAge = datetime.timedelta(seconds=maxAge)
    event_time = datetime.datetime.fromtimestamp(event["timestamp"])
    print(event_time)
    current_time = datetime.datetime.now()
    print(current_time)

    # Calculate the time difference in seconds
    time_difference = (current_time - event_time)

    # Evaluate the event timing and return the result
    if time_difference > maxAge:
        return time_difference, "message too old for matrix", False  # False indicates the event is too old
    else:
        return time_difference, "message timing is good", True  # True indicates the event is still valid
