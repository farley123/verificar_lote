import flet as ft

class ResultadoObservable:
    def __init__(self, initial_value=None):
        self._value = initial_value
        self._observers = []

    def subscribe(self, observer_func):
        self._observers.append(observer_func)

    def set(self, value):
        if value != self._value:
            self._value = value
            self._notify()

    def get(self):
        return self._value

    def _notify(self):
        for observer in self._observers:
            observer(self._value)

    def __str__(self):
        return str(self._value)
