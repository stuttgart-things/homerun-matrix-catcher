import asyncio
from event_source.event_source import EventSource


class StdinSource(EventSource):
    async def _read_stdin(self):
        """Continuously read from stdin and notify consumers."""
        print("Enter events (type 'exit' to quit):")
        print('Example event:  # event {"Mode":"Text","Args":{} }')
        while True:
            line = await asyncio.to_thread(input)  # Read input from stdin asynchronously
            await self._notify_consumers({"event": line})
            if line.strip().lower() == 'exit':
                break

    async def start(self):
        """Start the stdin event source."""
        print("In start")
        await self._read_stdin()

    async def stop(self):
        """Stop the stdin event source."""
        pass
