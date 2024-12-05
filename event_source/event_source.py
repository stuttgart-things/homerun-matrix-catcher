from abc import ABC, abstractmethod
from typing import Callable, Dict, List

class EventSource(ABC):
    def __init__(self):
        self.consumers: List[Callable[[str, Dict[str, str]], None]] = []

    def register_consumer(self, consumer: Callable[[str, Dict[str, str]], None]):
        """Register a consumer callback to be notified of new events."""
        self.consumers.append(consumer)

    @abstractmethod
    async def start(self):
        """Start the event source."""
        pass

    async def _notify_consumers(self, event: Dict[str, str]):
        """Notify all registered consumers about a new event."""
        for consumer in self.consumers:
            print(f"Notifying consumer: {consumer} with event: {event}")
            await consumer(event)
