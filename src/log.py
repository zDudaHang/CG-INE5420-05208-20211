from PyQt5.QtWidgets import QLabel


class Log(QLabel):
    def __init__(self):
        super().__init__()
        stylesheet = '''
            QLabel {
                background-color: white;
                border: 1px solid black
            }
        '''
        self.text = 'Log\n'
        self.setText(self.text)
        self.setStyleSheet(stylesheet)
    
    def add_log(self, text: str):
        self.text += f'{text}\n'
        self.setText(self.text)
