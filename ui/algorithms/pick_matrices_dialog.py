import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import numpy as np

from my_types.global_types import CtxDict

class PickMatricesDialog(qtw.QDialog):
    args_collected = qtc.Signal(list)

    def __init__(self, ctx: CtxDict,  names: tuple[str, ...], subtitle = ""):
        super().__init__()
        self.ctx = ctx
        if subtitle is None:
            self.setWindowTitle("Choose matrices")
        else:
            self.setWindowTitle(f"Choose matrices - {subtitle}")
        self.setMinimumWidth(300)
        self.form = qtw.QFormLayout()
        self.setLayout(self.form)

        self.combo_boxes = []
        for i in range(len(names)):
            combo_box = qtw.QComboBox()
            for j, _ in enumerate(ctx["matrices"]):
                combo_box.addItem(f"Matrix {j}")
            self.combo_boxes.append(combo_box)
            self.form.addRow(names[i], combo_box)

        self.submit = qtw.QPushButton("Ok")
        self.submit.clicked.connect(self.submit_matrices)
        self.form.addRow(self.submit)

    @qtc.Slot()
    def submit_matrices(self):
        matrices = []
        for combo_box in self.combo_boxes:
            matrix = self.ctx["matrices"][combo_box.currentIndex()]
            matrices.append(matrix)
        self.close()
        self.args_collected.emit(matrices)







