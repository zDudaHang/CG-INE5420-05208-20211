from PyQt5.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout
from typing import Generic, TypeVar

T = TypeVar('T')

class Log(QWidget, Generic[T]):
    def __init__(self, title: str):
        super().__init__()
        
        self.layout = QHBoxLayout()
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.scroll_area_content = QWidget()
        self.scroll_area_content.setGeometry( 0, 0, 600, 600 )
        self.scroll_area.setWidget(self.scroll_area_content)

        self.scroll_area_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area_layout.addWidget(QLabel(title))

        self.setLayout(self.layout)
    
    def add_item(self, item: T):
        self.scroll_area_layout.addWidget(QLabel(item.__str__()))

    def clear(self):
        for i in range(1, self.scroll_area_layout.count()):
            self.scroll_area_layout.itemAt(i).widget().deleteLater()
