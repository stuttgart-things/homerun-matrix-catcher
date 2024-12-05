import asyncio
from event_source.event_source import EventSource
from tests.generate_message import generate_random_event

class RandomEventSource(EventSource):
    async def get_events(self):
        """Generate a list of random events."""
        events = [generate_random_event() for _ in range(10)]  # Generate 10 random events
        print(f"Generated events: {events}")#######
        return events

    async def write_event(self, event):
        """Continuously read from stdin and notify consumers."""
        print(f"Writing event: {event}")#######
        await self._notify_consumers({"event": event})

    async def start(self):
        """Start the stdin event source."""
        print("In start")
        events = await self.get_events()
        for event in events:
            await self.write_event(event)
            await asyncio.sleep(5)
        await asyncio.sleep(120)

    async def stop(self):
        """Stop the stdin event source."""
        pass