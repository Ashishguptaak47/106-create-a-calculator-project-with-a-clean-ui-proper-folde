"""History and memory state manager for calculation sessions."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class HistoryItem:
    expression: str
    result: str


class HistoryManager:
    """Manages history log and calculator memory (MC, MR, M+, M-)."""

    def __init__(self, max_items: int = 50) -> None:
        self._history: List[HistoryItem] = []
        self._max_items = max_items
        self._memory: float = 0.0

    def add_entry(self, expression: str, result: str) -> None:
        """Record a completed calculation."""
        self._history.append(HistoryItem(expression=expression, result=result))
        if len(self._history) > self._max_items:
            self._history.pop(0)

    def get_entries(self) -> List[HistoryItem]:
        """Return full history in reverse order (most recent first)."""
        return list(reversed(self._history))

    def clear(self) -> None:
        """Clear all calculation history."""
        self._history.clear()

    # Memory features
    def memory_clear(self) -> None:
        self._memory = 0.0

    def memory_recall(self) -> float:
        return self._memory

    def memory_add(self, val: float) -> None:
        self._memory += val

    def memory_sub(self, val: float) -> None:
        self._memory -= val
