from __future__ import annotations
from abc import ABC, abstractmethod


class Context:

    _state = None

    def __init__(self, state):
        self.transition_to(state)

    def transition_to(self, state):
        self._state = state
        self._state.context = self

    def request1(self):
        self._state.handle1()

    def request2(self):
        self._state.handle2()


class State:

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @abstractmethod
    def handle1(self):
        pass

    @abstractmethod
    def handle2(self):
        pass


class ConcreteStateA(State):
    def handle1(self):
        self.context.transition_to(ConcreteStateB())

    def handle2(self):
        pass

class ConcreteStateB(State):
    def handle1(self):
        pass

    def handle2(self):
        self.context.transition_to(ConcreteStateA())


if __name__ == "__main__":
    # The client code.

    context = Context(ConcreteStateA())
    context.request1()
    context.request2()