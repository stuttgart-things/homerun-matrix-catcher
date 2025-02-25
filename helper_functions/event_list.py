
import asyncio
import sys
import datetime
from helper_functions.compare_time import evaluate_event_timing
from helper_functions.arguments import get_arguments
from display_on_matrix.image_gif.image import display_image

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
            pending_events += event_args
        print("\npending events")
        print(pending_events)
        print("\n\n")

async def run_event_list(self, pending_events, display_task, gen_gifs, maxtime):
    while True:
        print(f"evaluating pending events, {len(pending_events)} left")
        if pending_events:
            print("Popping event")
            event_args = pending_events.pop(0)
            print(f"Popped event: {event_args}")
            time_difference, log, not_expired = evaluate_event_timing(event_args, maxtime)
            print(log)
            print(f"The time difference is: {time_difference}")
            if not_expired:
                print(f"Running event: {event_args}")
                await display_task(event_args, gen_gifs)
            else:
                print("Events expired not showing")

        else:
            print("No events found, sleeping")
            args = {}
            args['image'] = "sthings.png"
            args['duration'] = "1"
            event = {
                "mode": "image",
                "severity": "INFO",
                "systems": "default",
                "timestamp": datetime.datetime.now().timestamp(),
                "args": args
                }
            await asyncio.create_task(self.display_image(args))
            await asyncio.sleep(0.05)
