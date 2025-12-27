"""
MANTIS - Event Bus
"""

from collections import defaultdict
from typing import Callable, Any


class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable[[Any], None]):
        """
        Subscribe a callback to an event.
        """
        self._subscribers[event_name].append(callback)

    def emit(self, event_name: str, payload: Any = None):
        """
        Emit an event to all subscribers.
        """
        for callback in self._subscribers.get(event_name, []):
            try:
                callback(payload)
            except Exception as e:
                print(f"[EVENT BUS] Error in '{event_name}' handler: {e}")
