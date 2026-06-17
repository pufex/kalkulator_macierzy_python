import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
from my_types.global_types import CtxDict

class LoadMenu(qtw.QDialog):
    matrices_loaded = qtc.Signal()

    def __init__(self, ctx: CtxDict):
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("Load matrices")

        self.layout = qtw.QVBoxLayout(self)
        self.setLayout(self.layout)

        self.buttonGroup = qtw.QButtonGroup(self)
        for i in range(ctx["f_manager"].n):
            button = qtw.QPushButton(f"Load file {i + 1}", self)
            self.buttonGroup.addButton(button, i + 1)
            self.layout.addWidget(button)
        self.buttonGroup.idClicked.connect(self.load_matrices)

    @qtc.Slot()
    def load_matrices(self, id: int):
        try:
            matrices = self.ctx["f_manager"].load_saved_file(id)
            self.ctx["matrices"].clear()
            self.ctx["matrices"] = matrices
        except:
            print(1)
            messageBox = qtw.QMessageBox()
            messageBox.setText("There was an error while loading up matrices.")
            messageBox.setIcon(messageBox.Icon.Critical)
            messageBox.exec()
            pass
        else:
            self.matrices_loaded.emit()
            self.close()