from typing import Callable
from PyQt5.QtWidgets import QWidget

class NewWidget():
    def __init__(self, widget: QWidget, get_value: Callable, clear: Callable):
        self.widget = widget
        self.get_value = get_value
        self.clear = clear