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



