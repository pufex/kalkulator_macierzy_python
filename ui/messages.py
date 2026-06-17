import PySide6.QtWidgets as qtw

class DefaultErrorMessageBox(qtw.QMessageBox):
    def __init__(self, text = "Something went wrong"):
        super().__init__()
        self.setWindowTitle("Error")
        self.setText(text)
        self.setIcon(qtw.QMessageBox.Icon.Critical)