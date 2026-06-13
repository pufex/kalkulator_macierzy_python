import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
from my_types.global_types import CtxDict

class SaveMenu(qtw.QDialog):
    def __init__(self, ctx: CtxDict):
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("Save matrices")

        self.layout = qtw.QVBoxLayout(self)
        self.setLayout(self.layout)

        self.button_group = qtw.QButtonGroup()
        for i in range(self.ctx["f_manager"].n):
            button = qtw.QPushButton(f"Save file {i + 1}")
            self.button_group.addButton(button, i + 1)
            self.layout.addWidget(button)
        self.button_group.idClicked.connect(self.save_matrices)

    @qtc.Slot()
    def save_matrices(self, id: int):
        try:
            self.ctx["f_manager"].save_to_file(id, self.ctx["matrices"])
        except:
            error_message_box = qtw.QMessageBox()
            error_message_box.setText(f"There was an error while saving your matrices to a file {id}")
            error_message_box.setIcon(qtw.QMessageBox.Icon.Critical)
            error_message_box.exec()
        else:
            self.close()