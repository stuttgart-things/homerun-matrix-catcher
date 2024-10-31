import asyncio
from event_source.event_source import EventSource


class JsonFileSource(EventSource):
    async def get_events(self,event_file):
        ### Test area for json file with event list.
        event_args = []
        with open(event_file, 'r') as file:
             event =  file.read()
        event = eval(event)

        return event["events"]

    async def write_event(self, event):
        """Continuously read from stdin and notify consumers."""
        await self._notify_consumers({"event": event})

    async def start(self,event_file):
        """Start the stdin event source."""
        print("In start")
        events = await self.get_events(event_file)
        for event in events:
            await self.write_event(event)
            await asyncio.sleep(45)
        await asyncio.sleep(200)

    async def stop(self):
        """Stop the stdin event source."""
        pass
