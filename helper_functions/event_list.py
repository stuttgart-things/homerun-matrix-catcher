
import asyncio
from helper_functions.compare_time import evaluate_event_timing
from helper_functions.arguments import get_arguments

async def build_event_list(queue, rules, pending_events):
    print("in build")
    while True:
        event_json = await queue.get()
        print(f"Processing event: {event_json}")
        event_args = get_arguments(rules, event_json["event"])
        print("*******************************************************************************************")
        print(event_args)
        print("*******************************************************************************************")
        if event_args:
            print("INSIDE HERE")
            pending_events += event_args
        print("\npending events")
        print(pending_events)
        print("\n\n")

async def run_event_list(pending_events, display_task):
    while True:
        print(f"evaluating pending events, {len(pending_events)} left")
        if pending_events:
            print("Popping event")
            event_args = pending_events.pop(0)
            print(f"Popped event: {event_args}")
            time_difference, log, event_expired = evaluate_event_timing(event_args, 120)
            print(log)
            print(f"The time difference is: {time_difference}")
            if event_expired:
                print(f"Running event: {event_args}")
                await display_task(event_args)
            else:
                print("Events expired not showing")

        else:
            print("No events found, sleeping")
            await asyncio.sleep(1)