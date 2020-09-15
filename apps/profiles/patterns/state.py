from __future__ import annotations
from abc import ABC, abstractmethod


class ContextState:
    _state = None

    def __init__(self, state):
        self.transition_to(state)

    def transition_to(self, state):
        self._state = state
        self._state.context = self

    def request1(self, data):
        print(data)
        self._state.handle1(data)

    def request2(self, data):
        self._state.handle2(data)


class State:

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @abstractmethod
    def handle1(self, data):
        pass

    @abstractmethod
    def handle2(self, data):
        pass
