
from dataclasses import dataclass
from enum import Enum

from collections import deque

from heapq import heappop, heappush
from itertools import count


class PriorityLevel(Enum):
    CRITICAL = 3
    IMPORTANT = 2
    NEUTRAL = 1
    Low = 0


@dataclass
class Message:
    event: str


@dataclass
class Event:
    topic: str
    message: Message
    priority_level: PriorityLevel = PriorityLevel.NEUTRAL


class IterableMixin:
    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        while len(self) > 0:
            yield self.dequeue()


class Queue(IterableMixin):
    def __init__(self, *elements):
        self._elements = deque(elements)

    @property
    def elements(self):
        return self._elements

    def enqueue(self, element):
        self._elements.append(element)

    def dequeue(self):
        return self._elements.popleft()


class Stack(Queue):
    def dequeue(self):
        return self._elements.pop()


class PriorityQueue(IterableMixin):
    def __init__(self):
        self._elements = []
        self._counter = count()

    @property
    def elements(self):
        return self._elements

    def enqueue_with_priority(self, priority, value):
        element = (-priority, next(self._counter), value)
        heappush(self._elements, element)

    def dequeue(self):
        return heappop(self._elements)[-1]
