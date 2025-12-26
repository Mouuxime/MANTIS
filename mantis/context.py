"""
MANTIS Context
Global shared state
"""

from typing import Any, Dict


class Context:
    def __init__(self):
        self._data: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def has(self, key: str) -> bool:
        return key in self._data

    def remove(self, key: str):
        if key in self._data:
            del self._data[key]

    def dump(self) -> Dict[str, Any]:
        """
        Returns a copy of the context (for debug/logging).
        """
        return dict(self._data)
