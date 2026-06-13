import PySide6.QtWidgets as qtw

class DefaultErrorMessageBox(qtw.QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Error")
        self.setText("Something went wrong")
        self.setIcon(qtw.QMessageBox.Icon.Critical)