from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List
import datetime


class Subject:
    _observers = []

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, **kargs):
        for observer in self._observers:
            observer.update(self, **kargs)


class Observer:

    def update(self, subject):
        pass
