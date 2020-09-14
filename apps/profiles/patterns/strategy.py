from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Context:

    def __init__(self, strategy):
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    def do_some_business_logic(self, data):
        result = self._strategy.do_algorithm(data)


class Strategy:
    def do_algorithm(self, data):
        pass


class ConcreteStrategyA(Strategy):
    def do_algorithm(self, data):
        print(sorted(data))
        return sorted(data)


class ConcreteStrategyB(Strategy):
    def do_algorithm(self, data):
        print(data)
        return reversed(sorted(data))


if __name__ == "__main__":
    # The client code picks a concrete strategy and passes it to the context.
    # The client should be aware of the differences between strategies in order
    # to make the right choice.

    context = Context(ConcreteStrategyA())
    print("Client: Strategy is set to normal sorting.")
    context.do_some_business_logic([1, 2, 3, 4, 5])
    print()

    print("Client: Strategy is set to reverse sorting.")
    context.strategy = ConcreteStrategyB()
    context.do_some_business_logic([1, 2, 3, 4, 5])
